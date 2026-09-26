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
  矢印キーでめくってください
</div>

---
layout: default
---

# 前提：「MVVM ＝ データバインディング」ではない

まず、議論の土台としてよくある誤解を解いておきます。

<br>

<div class="grid grid-cols-2 gap-6 pt-2">

<div class="p-4 border border-blue-500/30 rounded-xl bg-blue-500/5">
  <h3 class="font-bold text-blue-400 mb-2">🎯 本質は「責務の分割」</h3>
  <ul class="text-xs space-y-2 text-gray-300">
    <li>Viewから表示ロジックを剥がすためのパターン</li>
    <li>DataBinding / Rx / Command は<b>「接続の実装手段」</b>に過ぎない</li>
    <li>Binding責務はどこにあってもいい<br>（Engine、Binder、View自身の <code>Initialize</code>）</li>
  </ul>
</div>

<div class="p-4 border border-emerald-500/30 rounded-xl bg-emerald-500/5">
  <h3 class="font-bold text-emerald-400 mb-2">📦 ImmutableでもMVVM</h3>
  <ul class="text-xs space-y-2 text-gray-300">
    <li>「Rxを使っていないからMVVMじゃない」ではない</li>
    <li>後から値が変わらないステータス画面なら、<br><b>readonly struct を <code>Initialize</code> で渡すだけ</b>でも十分にMVVM！</li>
  </ul>
</div>

</div>

<br>

> 💡 **「ReactivePropertyを使っているからMVVM」なのではありません。**

---
layout: default
---

# そもそもViewModelとは何か？

Viewの具体的な見た目（ピクセルや色）ではなく、<br>
**「Viewが論理的に取りうる状態」をモデル化したもの**。

<br>

```text
[ Model / Domain ]
       │
       ▼ ModelをPresentation上意味のある状態へ射影
[ ViewModel ]
   CurrentHp / MaxHp  ➔  HpRate (割合)  ➔  IsDanger (危険域判定)
       │
       ▼ 画面へのレンダリング
[ View ]
   「赤く点滅させる」「マテリアルを切り替える」「シェイクさせる」
```

<br>

- `IsDanger` までは **ViewModel**（UIロジック・テスト可能）
- `赤くする・点滅させる` は **View**（描画の具象）
- ViewModelは単なるModelのコピーではなく、**Presentationのために射影されたモデル**。

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
**「Presentation DomainそのもののModel（正準形式）」**である。

<div class="mt-3 text-emerald-400 font-bold text-sm">
  「ViewをViewModelの従属変数にできる領域」ほど、MVVMは綺麗に成立する！
</div>

</div>

</div>

---
layout: default
---

# 【第1の壁】ゲームには「演出という時間」がある

ここからがゲーム特有の難しさです。例えばソシャゲの**限界突破（凸）**。

<br>

<div class="p-5 border border-amber-500/40 rounded-xl bg-amber-500/10">

### 📱 こんな経験、ありませんか？

「凸する」ボタンを押した瞬間……<br>
画面が暗転フェードする前の**ほんの1フレーム**だけ、<br>
<span class="text-red-400 font-bold text-lg">すでに凸後の「★4」にUIが更新されてネタバレしている！</span>

</div>

<br>
<v-click>

- なぜあんなカッコ悪いことが起きるのか？
- **「Modelが変わったら即座に画面へ自動反映すべき」というナイーブな即時同期で一番よく起きる事故です。**

</v-click>

---
layout: default
---

# なぜ起きる？：「Domain」と「Presentation」の時間のズレ

ゲームでは、**データの確定**と**画面の見せ方**の時間軸が一致しません。

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
- 「ModelとVMを無邪気に自動同期した」結果、演出が破壊される。

> 🚨 **「正しい値なのに、正しいタイミングではない」** という時間軸の衝突！

</v-click>

---
layout: default
---

# 解決策：2つの「commit」を分離する

View ↔ ViewModel のバインディングはそのままでいい。<br>
切るべきなのは、**「Model ➔ ViewModel の無条件・即時追従」**です。

<br>

```csharp {all|1-2|4|6|all}
// ① UseCase完了 ＝ 【Domain上のcommit】
// （裏でModel層は3凸に更新されるが、ViewModelはまだ更新しない！）
var result = await useCase.LimitBreakAsync();

// ② 演出進行（ムービー再生・フェード。画面はまだ2凸のまま待つ！）
await PlayPresentationAsync(result);

// ③ 【Presentation上のcommit】（★演出が終わった瞬間に手動で同期！）
viewModel.Apply(result); // ➔ これに伴ってViewが3凸に切り替わる！

await FadeInAsync();
```

<br>

- **Domainのcommit** と **Presentationのcommit** の間に「演出時間」を挟む
- 同期タイミングを、async/awaitなどの**手続き（シーケンス）**が調停する

---
layout: default
---

# 【第2の壁】インゲームでは「Viewが単なるViewではない」

さらに画面を飛び出して3D空間・ゲームプレイに入ると、もう1つの壁が現れます。

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

これらは受動的な描画先ではなく、**「自身が状態を持ち、時間発展するシステム」**です。

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

# 歩く3Dモデルは「View」なのか？

Unityでよく悩む、命名と責務の違和感の正体。

<br>

<div class="grid grid-cols-2 gap-6 pt-2">

<div class="p-4 border border-red-500/30 rounded-xl bg-red-500/5">
  <h4 class="font-bold text-red-400 mb-1">❌ <code>PlayerModel : MonoBehaviour</code></h4>
  <p class="text-xs text-gray-300">
    ドメインモデルのはずが、Transformを持ち、シーンにぶら下がり、テストもできない。
  </p>
</div>

<div class="p-4 border border-red-500/30 rounded-xl bg-red-500/5">
  <h4 class="font-bold text-red-400 mb-1">❌ <code>PlayerView : MonoBehaviour</code></h4>
  <p class="text-xs text-gray-300">
    受動的な描画のはずが、Lスティック入力を受け、CharacterControllerで物理衝突を解いている。
  </p>
</div>

</div>

<br>

<v-click>

### 💡 違和感の答え：彼らは「View」でも「Model」でもない
- 二世界のラベル（Model / View）を無理やり貼ろうとするから歪む。
- 彼は **「World Simulation（シミュレーション世界）」という第3の世界に生きる『Actor / Entity』** である！

</v-click>

---
layout: default
---

# ゲームに君臨する「3つの世界（三世界モデル）」

ゲームのアーキテクチャは、本質的にこの**3層構造**で動いています。

<br>

```text
【1. Persistent Domain】（永続的なゲームルール）
    所持金、アイテム、キャラの凸段階、クエスト進行フラグ
              │
              ▼ 意味の伝播
【2. World Simulation】（毎フレーム時間発展する物理世界）★ゲーム特有！
    Transform、Rigidbody、コライダー、アニメーション遷移、移動入力
              │
              ▼ 提示の同期
【3. Presentation】（提示と演出の世界）
    カメラ演出、カットシーン、SE再生、uGUI、画面フェード
```

<br>

> 🚨 **ゲームの主役は、DomainとPresentationの間で蠢く「World Simulation」である！**  
> GUIアプリ用の「二世界（Domain ➔ Presentation）」の枠組みに押し込もうとするから破綻する。

---
layout: default
---

# 境界の深淵：「Domainは判定できるが、観測できない」

クエスト「特定地点に到達したら進行」で直面する壁。

<br>

```text
仕様:「神殿の入口から半径5m以内に到達したら進行」
```

<br>

```text
1. Observation（物理観測 / Simulation）
   Transform.position = (127.3, 2.0, -83.5)
      ↓
2. Spatial interpretation（空間解釈 / Simulation）
   IsInsideArea(A) == true  ➔  EnteredArea(A) イベント発生！
      ↓ ─── semantic boundary ───
3. Domain interpretation（ドメイン解釈 / Domain）
   HasReached(AncientGate) = true （永続的ドメイン事実）
```

<br>

<div class="text-xs text-gray-300">

- **OnTriggerEnter一発で済ませると起きる悲劇**:
  - セーブ＆ロード時、プレイヤーがすでにエリア内にリスポーンしたら発火せず進行不能に！
- Domainは「到達したら進行」という**ルールを判定できるが、自前で観測はできない**。
- この多層の意味境界（Semantic Boundary）を、MVVMの自動バインディングで繋ぐことはできない。

</div>

---
layout: default
---

# MVVMが向く場所・向かない場所（適材適所）

2つの壁（時間・空間）を踏まえた、明確な境界線。

<br>

<div class="grid grid-cols-2 gap-6">

<div class="p-4 border-2 border-emerald-500/50 rounded-xl bg-emerald-500/5">
  <h3 class="text-emerald-400 font-bold mb-2">⭕ 向いている領域（アウトゲーム）</h3>
  <ul class="text-xs space-y-2 text-gray-300">
    <li>設定、ショップ、インベントリ、ステータス画面</li>
    <li><b>二世界（Domain ➔ Presentation）で完結する</b></li>
    <li>ViewをViewModelの従属変数にできる</li>
    <li>二重状態が発生せず、テスタビリティの恩恵大！</li>
  </ul>
</div>

<div class="p-4 border-2 border-red-500/50 rounded-xl bg-red-500/5">
  <h3 class="text-red-400 font-bold mb-2">❌ 向かない領域（インゲーム・演出）</h3>
  <ul class="text-xs space-y-2 text-gray-300">
    <li>3Dキャラ操作、戦闘、カットシーン</li>
    <li><b>三世界（World Simulation）が介在する</b></li>
    <li>View自身が状態を持って時間発展し、時間軸もズレる</li>
    <li>無理にMVVMに押し込まず、Actor / 手続きを使おう</li>
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
- **ゲーム全体をMVVMの二世界モデルに押し込もうとするのが間違い**
  - 画面と問題の性質を見極め、アウトゲームにはMVVM、インゲームにはActor/手続きを使い分けよう！

</div>

---
layout: center
class: text-center
---

# ご清聴ありがとうございました 🙌

質問・ご意見など大歓迎です！
