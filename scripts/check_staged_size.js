const fs = require('fs');
const { execSync } = require('child_process');

// 50MB (GitHubのWarningライン。100MBで完全ブロック)
const MAX_BYTES = 50 * 1024 * 1024;

try {
  // ステージングされているファイル一覧を取得 (追加・コピー・変更されたファイル)
  const output = execSync('git diff --cached --name-only --diff-filter=ACM', { encoding: 'utf-8' });
  const files = output.split(/\r?\n/).filter(Boolean);

  let hasError = false;

  for (const file of files) {
    if (fs.existsSync(file)) {
      const stats = fs.statSync(file);
      if (stats.size > MAX_BYTES) {
        const mb = (stats.size / (1024 * 1024)).toFixed(1);
        console.error('\n\x1b[31m===============================================================\x1b[0m');
        console.error(`\x1b[31m❌ [Commit Blocked] 巨大ファイルが検出されました！\x1b[0m`);
        console.error(`   対象ファイル : \x1b[33m${file}\x1b[0m (\x1b[31m${mb} MB\x1b[0m)`);
        console.error(`   安全上限     : 50.0 MB (GitHubの警告ライン / 100MBでpush拒否)`);
        console.error('\x1b[31m===============================================================\x1b[0m');
        console.error('\x1b[36m💡 対処方法:\x1b[0m');
        console.error(`   1. ステージングを解除します:`);
        console.error(`      \x1b[32mgit reset HEAD "${file}"\x1b[0m`);
        console.error(`   2. 動画編集ツール等でトリミング・圧縮してから再度追加してください。\n`);
        hasError = true;
      }
    }
  }

  if (hasError) {
    process.exit(1);
  }
} catch (err) {
  if (err.status) {
    process.exit(err.status);
  }
}
