import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';
import { parse } from '@slidev/parser';
import PptxGenJS from 'pptxgenjs';

const ROOT_DIR = process.cwd();
const DIST_DIR = path.join(ROOT_DIR, 'dist');
const SLIDES_DIR = path.join(DIST_DIR, 'slides');
const GIFS_DIR = path.join(DIST_DIR, 'gifs');
const OUTPUT_PPTX = path.join(DIST_DIR, 'slides.pptx');
const SLIDES_MD = path.join(ROOT_DIR, 'slides.md');

async function main() {
  console.log('🚀 Starting PPTX export with animated GIFs...');

  // 1. Prepare directories
  fs.mkdirSync(DIST_DIR, { recursive: true });
  fs.mkdirSync(GIFS_DIR, { recursive: true });

  // 2. Parse slides.md to find video references and notes
  console.log('📄 Parsing slides.md...');
  const mdContent = fs.readFileSync(SLIDES_MD, 'utf-8');
  const parsed = await parse(mdContent);
  const slides = parsed.slides;
  console.log(`Found ${slides.length} slides.`);

  const videoMap = new Map(); // slideNumber (1-based) -> videoSrc
  slides.forEach((slide, idx) => {
    const slideNo = idx + 1;
    const videoMatch = slide.content.match(/<video[^>]+src=["']([^"']+)["']/);
    if (videoMatch) {
      videoMap.set(slideNo, {
        src: videoMatch[1],
        content: slide.content,
      });
      console.log(`  - Slide ${slideNo}: found video ${videoMatch[1]}`);
    }
  });

  // 3. Convert referenced videos to animated GIFs using ffmpeg
  console.log('\n🎞️  Converting videos to animated GIFs...');
  const gifMap = new Map(); // videoSrc -> gifPath
  for (const [slideNo, { src }] of videoMap.entries()) {
    // Resolve local path (e.g. /videos/foo.mov -> public/videos/foo.mov)
    const relPath = src.startsWith('/') ? src.slice(1) : src;
    const inputVideoPath = path.join(ROOT_DIR, 'public', relPath);

    if (!fs.existsSync(inputVideoPath)) {
      console.warn(`⚠️ Video not found: ${inputVideoPath}`);
      continue;
    }

    const baseName = path.basename(inputVideoPath, path.extname(inputVideoPath));
    const outputGifPath = path.join(GIFS_DIR, `${baseName}.gif`);
    gifMap.set(src, outputGifPath);

    // Check cache
    const shouldConvert =
      !fs.existsSync(outputGifPath) ||
      fs.statSync(inputVideoPath).mtimeMs > fs.statSync(outputGifPath).mtimeMs;

    if (shouldConvert) {
      console.log(`  Converting ${path.basename(inputVideoPath)} -> ${baseName}.gif...`);
      // 12fps, width 480px, 128 colors palette for compact size & smooth loop
      const cmd = `ffmpeg -y -i "${inputVideoPath}" -vf "fps=12,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse=dither=bayer" "${outputGifPath}"`;
      try {
        execSync(cmd, { stdio: 'pipe' });
        const sizeMb = (fs.statSync(outputGifPath).size / (1024 * 1024)).toFixed(2);
        console.log(`  ✓ Converted (${sizeMb} MB)`);
      } catch (err) {
        console.error(`  ❌ Failed to convert video: ${err.message}`);
      }
    } else {
      console.log(`  ⚡ Using cached GIF: ${baseName}.gif`);
    }
  }

  // 4. Export slides as PNGs using Slidev CLI
  console.log('\n📸 Exporting slide images with Slidev...');
  execSync(`npx slidev export --format png --output dist/slides`, {
    stdio: 'inherit',
  });

  // 5. Build PPTX presentation using pptxgenjs
  console.log('\n📦 Assembling PPTX with animated GIFs...');
  const pptx = new PptxGenJS();
  pptx.layout = 'LAYOUT_16x9'; // 10 x 5.625 inches
  const SLIDE_WIDTH = 10.0;
  const SLIDE_HEIGHT = 5.625;

  for (let i = 1; i <= slides.length; i++) {
    const pngPath = path.join(SLIDES_DIR, `${i}.png`);
    if (!fs.existsSync(pngPath)) {
      console.warn(`⚠️ Slide image missing: ${pngPath}`);
      continue;
    }

    const pptSlide = pptx.addSlide();

    // 1) Background slide image (full-bleed)
    pptSlide.addImage({
      path: pngPath,
      x: 0,
      y: 0,
      w: '100%',
      h: '100%',
    });

    // 2) Presenter note if present
    const note = slides[i - 1]?.note;
    if (note) {
      pptSlide.addNotes(note.trim());
    }

    // 3) Overlay animated GIF if this slide contains a video
    if (videoMap.has(i)) {
      const { src, content } = videoMap.get(i);
      const gifPath = gifMap.get(src);

      if (gifPath && fs.existsSync(gifPath)) {
        // Inspect GIF dimensions
        let aspect = 16 / 9;
        try {
          const probe = execSync(
            `ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 "${gifPath}"`,
            { encoding: 'utf-8' }
          ).trim();
          const [gw, gh] = probe.split('x').map(Number);
          if (gw && gh) aspect = gw / gh;
        } catch (_) {}

        // Target placement on right column
        const width = SLIDE_WIDTH * 0.43; // ~4.3 inches
        const height = width / aspect;
        const x = SLIDE_WIDTH * 0.512; // ~5.12 inches

        // Slight vertical offset adjustment if bottom footnote text exists
        const hasFootnote = content.includes('text-xs text-gray-400') || content.includes('※');
        const y = hasFootnote ? 1.52 : 1.8;

        pptSlide.addImage({
          path: gifPath,
          x,
          y,
          w: width,
          h: height,
        });
        console.log(`  ✓ Embedded GIF into slide ${i} (${width.toFixed(2)}" x ${height.toFixed(2)}")`);
      }
    }
  }

  // 6. Write final PPTX file
  await pptx.writeFile({ fileName: OUTPUT_PPTX });
  const totalMb = (fs.statSync(OUTPUT_PPTX).size / (1024 * 1024)).toFixed(2);
  console.log(`\n🎉 Successfully exported PPTX: ${OUTPUT_PPTX} (${totalMb} MB)`);
  console.log('💡 Upload dist/slides.pptx to Google Drive and open with Google Slides to present with animations!');
}

main().catch((err) => {
  console.error('Fatal error during export:', err);
  process.exit(1);
});
