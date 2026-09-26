---
theme: default
background: https://cover.sli.dev
title: MVVMはなぜゲームに向かないと言われがちなのか
info: |
  ## MVVMはなぜゲームに向かないと言われがちなのか
  「状態の表示」と「時間発展する世界」の境界線
class: text-center
drawings:
  persist: false
transition: slide-left
mdc: true
---

# MVVMはなぜゲームに<br><span class="text-red-400">向かない</span>と言われがちなのか？

〜 「状態の表示」と「時間発展する世界」の境界線 〜

<div class="pt-8 text-sm opacity-60">
  5分LT / 矢印キーでめくってください
</div>

---
layout: default
---

# まず前提：「MVVM ＝ データバインディング」ではない

よくある誤解ですが、MVVMは**「責務分割」**の考え方です。

<br>

<div class="grid grid-cols-2 gap-6 pt-2">

<div class="p-4 border border-blue-500/30 rounded-xl bg-blue-500/5">
  <h3 class="font-bold text-blue-400 mb-2">🎯 本質：責務の分離</h3>
  <ul class="text-xs space-y-2 text-gray-300">
    <li>Viewからロジックを剥がすためのパターン</li>
    <li>DataBinding / Rx / Command は<b>「接続の実装手段」</b>に過ぎない</li>
    <li>Binding責務はどこにあってもいい<br>（Engine、Binder、View自身の <code>Initialize</code>）</li>
  </ul>
</div>

<div class="p-4 border border-emerald-500/30 rounded-xl bg-emerald-500/5">
  <h3 class="font-bold text-emerald-400 mb-2">📦 ImmutableでもMVVM</h3>
  <ul class="text-xs space-y-2 text-gray-300">
    <li>「Rxを使っていないからMVVMじゃない」ではない</li>
    <li>操作で値が変わらないステータス画面なら、<br><b>readonly struct を <code>Initialize</code> で渡すだけ</b>でも十分にMVVM的！</li>
  </ul>
</div>

</div>

<br>

> 💡 **Mutable（Reactive）とImmutable（struct）の違いは、時間方向の変化をどう表現するかの違いに過ぎない。**

---
layout: default
---

# そもそもViewModelとは何か？

Viewの具体的な見た目ではなく、<br>
**「Viewが論理的に取りうる状態」をモデル化したもの**。

<br>

```text
[ Model / Domain ]
       │
       ▼ ModelをPresentation上意味のある状態へ射影
[ ViewModel ]
   CurrentHp / MaxHp  ➔  HpRate (割合)  ➔  IsDanger (論理判定)
       │
       ▼ 画面へのレンダリング
[ View ]
   「赤く点滅させる」「マテリアルを切り替える」「Tweenさせる」
```

<br>

- `IsDanger` までは **ViewModel**（UIロジック・テスト可能）
- `赤くする・点滅させる` は **View**（描画の具象）
- ViewModelは「Modelのコピー」ではなく、**Presentationのために射影されたモデル**。

---
layout: two-cols
---

# M と VM/V の間にある「大きな境界」

Model層とPresentation層は、同質なレイヤーではありません。

```text
  Domain / Model (ゲーム世界の状態)
═══════════════════════════════════════ boundary
  Presentation (提示の問題領域)
      ViewModel (PresentationのModel)
          ↓
        View
```

### Presentationにしか存在しない状態がある
- 例：パーティ画面の **`SelectedMemberIndex`**
  - 「AliceとBobがいる」➔ **Domainの事実**
  - 「今Bobのタブを開いている」➔ **Presentationだけの事実**

::right::

<div class="pl-4 pt-10">

<div class="p-4 border border-amber-500/30 rounded-xl bg-amber-500/10">

### 💡 重要な真理

ViewModelは単なるDomainのアダプタではなく、<br>
**「Presentation DomainそのもののModel」**である。

<div class="mt-3 text-emerald-400 font-bold text-sm">
  「ViewをViewModelの従属変数にできる領域」ほど、MVVMは綺麗に成立する！
</div>

</div>

</div>

---
layout: default
---

# しかしゲームでは「Viewが単なるViewではない」

一般的なGUIと違い、ゲームのView側コンポーネントは……

<br>

<div class="grid grid-cols-3 gap-3 font-mono text-center text-xs">
  <div class="p-2 bg-gray-800 rounded">Transform</div>
  <div class="p-2 bg-gray-800 rounded">Animator</div>
  <div class="p-2 bg-gray-800 rounded">Rigidbody</div>
  <div class="p-2 bg-gray-800 rounded">NavMeshAgent</div>
  <div class="p-2 bg-gray-800 rounded">ParticleSystem</div>
  <div class="p-2 bg-gray-800 rounded">Timeline / Playable</div>
</div>

<br>

これらは単なる描画先ではなく、**「自身が状態を持ち、時間発展するシステム」**です。

<br>

<v-click>

### 🚨 その状態までViewModelに持ち込むとどうなるか？
- `ViewModel.Position` と `Transform.position` の**二重管理**
- `ViewModel.AnimationState` と `Animator` の**二重管理**
- ➔ **「どっちが正本（canonical）なのか？ どう同期するのか？」** という泥沼が始まる！

</v-click>

---
layout: default
---

# さらに「Domainの時間」と「Presentationの時間」がズレる

ソシャゲの「凸（限界突破）演出」の例。

<br>

```text
Domain（確定データ）:
    API完了 ────────────────────────────── 3凸に確定！

Presentation（画面演出）:
    2凸 ── フェード ── 昇格ムービー ── reveal ── 3凸を表示！
```

<br>

<v-click>

- **ここで Model ➔ ViewModel を無条件に即時バインディングすると？**
  - APIが完了した瞬間、フェード前に画面が「3凸」に書き換わりネタバレする！
- MVVMの自動同期が正しく働いた結果、演出が破壊される。

> 🚨 **「正しい値なのに、正しいタイミングではない」** という問題が発生する。

</v-click>

---
layout: default
---

# したがって「常時同期」すればよいわけではない

View ↔ ViewModel のバインディングはそのままでいい。<br>
切るべきなのは、**「Model ➔ ViewModel の無条件・即時追従」**です。

<br>

```csharp {all|1-2|4|6|all}
// ① UseCase完了 ＝ 【Domain上のcommit】（データは3凸になる）
var result = await useCase.LimitBreakAsync();

// ② 演出進行（ムービー再生・フェードなど。画面はまだ2凸のまま待つ！）
await PlayPresentationAsync(result);

// ③ 【Presentation上のcommit】（★ここで手動で同期する！）
viewModel.Apply(result); // ➔ これに伴ってViewが3凸に切り替わる

await FadeInAsync();
```

<br>

- **Domainの確定** と **Presentationの確定** を別々のタイミングで行う
- これを手続き（async/await）で調停する

---
layout: default
---

# MVVMが向く場所・向かない場所

<br>

<div class="grid grid-cols-2 gap-6">

<div class="p-4 border-2 border-emerald-500/50 rounded-xl bg-emerald-500/5">
  <h3 class="text-emerald-400 font-bold mb-2">⭕ 向いている領域（アウトゲーム）</h3>
  <ul class="text-xs space-y-2 text-gray-300">
    <li>設定、ショップ、インベントリ、ステータス画面</li>
    <li><b>ViewをViewModelの従属変数にできる領域</b></li>
    <li>View側に独自の複雑な時間発展（物理・NavMesh等）がない</li>
    <li>二重状態が発生せず、MVVMが最高に輝く！</li>
  </ul>
</div>

<div class="p-4 border-2 border-red-500/50 rounded-xl bg-red-500/5">
  <h3 class="text-red-400 font-bold mb-2">❌ 向かない領域（インゲーム・演出）</h3>
  <ul class="text-xs space-y-2 text-gray-300">
    <li>3Dキャラ操作、戦闘、カットシーン</li>
    <li><b>View自身が物理やアニメーションの状態を持つ</b></li>
    <li>DomainとPresentationで時間軸がズレる</li>
    <li>無理に状態同期に押し込めると、二重管理とライフサイクル問題が噴出する</li>
  </ul>
</div>

</div>

---
layout: default
---

# まとめ：一番短い答え

<br>

<div class="p-6 border-2 border-amber-500/50 rounded-xl bg-amber-500/10 text-center my-4">
  <div class="text-xl font-bold leading-relaxed">
    MVVMが得意なのは、<span class="text-emerald-400">「状態を表示すること」</span>。<br>
    ゲームが難しいのは、<span class="text-red-400">「表示そのものにも状態と時間があること」</span>。
  </div>
</div>

<br>

<div class="text-sm space-y-2 text-gray-300">

- **MVVMがゲームに向かないのではない**
  - 「Presentationの論理状態をVMに置き、Viewをその投影にできる問題」には最高に向いている。
- **ゲーム全体をMVVMに押し込もうとするのが間違い**
  - 画面の性質を見極め、アウトゲームにはMVVM、インゲームにはActor/手続きを使い分けよう！

</div>

---
layout: center
class: text-center
---

# ご清聴ありがとうございました 🙌

質問・ご意見など大歓迎です！
