---
theme: default
title: MVVMはなぜゲームに向かないと言われがちなのか
info: |
  ## MVVMはなぜゲームに向かないと言われがちなのか
class: text-center
drawings:
  persist: false
transition: slide-left
mdc: true
---

# MVVMはなぜゲームに<br><span class="text-red-400">向かないと言われがち</span>なのか

<div class="pt-6 text-lg opacity-85">
MVVMを否定する話ではなく、<br>ゲームでどう活かすかの話
</div>

<!--
- MVVMそのものを否定する話ではない
- むしろMVVMをゲームでどう活かすかの話
- 軸：ViewModelを表示用データではなく、Viewの仕様上取りうる論理状態として見る
- 後半：ゲームにはPresentationだけでなく、Simulationという状態空間もある
-->

---
layout: default
---

# MVVMとは

<div class="p-5 border border-emerald-500/40 rounded-xl bg-emerald-500/10">

```text
Model
  アプリケーション／ゲーム上の状態・ルール
      ↓ presentation向けに解釈する
ViewModel
  Viewの仕様上取りうる論理状態
      ↓ binding / observe
View
  ViewModelの状態を具体的な見た目・操作として表現する
```

</div>

<br>

実装では **Binding**（データバインディング）で ViewModel と View を結ぶことが多い。

<!--
- MVVMの基本：Model / ViewModel / View の三層
- Model：アプリケーション／ゲーム上の状態・ルール
- ViewModel：Viewの仕様上取りうる論理状態
- View：その状態を具体的な見た目や操作として表現するもの
- BindingはVM→Viewを結ぶ代表的な仕組み
- MVVMの本質をBindingだけに置かない
-->

---
layout: default
---

# ViewModelとは

**Viewの挙動・仕様をモデル化するもの**

<br>

<div class="p-5 border border-emerald-500/40 rounded-xl bg-emerald-500/10">

## ViewModelが表すもの

```text
この画面は、仕様上どんな状態を取りうるか
その状態では、何が表示され、何が操作可能か
その状態から、どの操作で次の状態へ移るか
```

</div>

<br>

<div class="text-xl font-bold">
ViewModelは、Presentationの状態空間を型で表現する。
</div>

<!--
- ViewModelを表示用データの入れ物として見ない
- Viewの挙動や仕様をモデル化するものとして見る
- 「仕様上取りうる状態」を明示する
- できれば型で表現する
- ありえない画面状態を作りにくくする
-->

---
layout: default
---

# MVPとMVVMの違い

<div class="grid grid-cols-2 gap-6">

<div class="p-5 border border-blue-500/30 rounded-xl bg-blue-500/5">

## MVP

```text
Presenter
  ├─ view.SetHpText("23/100")
  ├─ view.SetGauge(0.23)
  └─ view.ShowDanger()
```

Viewをどう変更するかを指示する。

</div>

<div class="p-5 border border-emerald-500/30 rounded-xl bg-emerald-500/5">

## MVVM

```text
ViewModel
  ├─ HpText = "23/100"
  ├─ HpRate = 0.23
  └─ IsDanger = true
        ↓ binding
View
```

Viewがどういう状態であるべきかを表す。

</div>

</div>

<!--
- MVP：Viewへの操作をPresenterが指示する
- MVVM：Viewがあるべき状態をViewModelとして表す
- どちらでも実装上は混ざりうる
- この発表では設計の重心を見る
- MVVMはPresentationを状態空間として扱いやすい
-->

---
layout: center
class: text-center
---

# MVVMの強みは<br><span class="text-emerald-400">宣言的なPresentation State</span>

<div class="pt-8 text-xl opacity-80">
「Viewに何をさせるか」ではなく<br>
「Viewは今どういう状態であるべきか」を表す
</div>

<!--
- MVVMを推す理由をここで明確にする
- Bindingそのものではなく、Presentationを宣言的な状態として表せること
- View更新の命令列ではなく、現在の画面状態を見る
- 状態として表すことで、仕様・テスト・再描画・復元を扱いやすくなる
-->

---
layout: default
---

# Modelの値をPresentation向けに解釈する

```text
Model側
  PlayerHp = 23 / 100
        │
        ▼  presentation向けに解釈する
ViewModel
  HpText = "23/100"
  HpRate = 0.23
  IsDanger = true
        │
        ▼  binding / observe
View
  ゲージ幅を23%にする
  危険状態として強調する
```

<br>

ViewModelは、Modelのコピーではなく、**Presentationにとって意味のある状態**を持つ。

<!--
- HPの例
- Modelの値をそのまま流すだけではない
- Viewにとって意味のある状態へ変換する
- HpText、HpRate、IsDangerはPresentationの論理状態
- Viewはそれを具体的な見た目へ変換する
-->

---
layout: default
---

# Presentationにしかない状態

<div class="grid grid-cols-2 gap-6 items-center">

<div>

例：パーティーステータス画面。

```text
Model側
  PartyMembers = [Alice, Bob, Carol, Dave]
        ↓
ViewModel
  SelectedMemberIndex = 3
  SelectedMember = Dave
        ↓ binding
View
  Daveのステータスを表示
  Daveのタブを選択状態にする
```

<div class="p-3 border border-emerald-500/40 rounded-xl bg-emerald-500/10 text-sm mt-3">

**「今Dave（4人目）を見ている」は、ゲーム世界の事実ではない。**  
それはPresentationの状態です。

</div>

</div>

<div>
  <img src="/images/party_status_tabs.png" class="rounded-xl border border-white/10 shadow-lg w-full" alt="4人パーティのステータス画面で4人目のタブが選択されている" />
  <div class="text-xs text-gray-400 mt-2 text-center">スクショは4人目のメンバーを表示している</div>
</div>

</div>

<!--
- Presentationにしかない状態の例
- パーティメンバーの存在はゲーム世界の事実
- どのメンバーを見ているかはPresentationの状態
- ViewModelはこの状態を持てる
- MVVMが得意な領域
-->

---
layout: default
---

# 仕様上取りうる状態を型で表す

<div class="grid grid-cols-2 gap-6">

<div>

画面状態を型にすると、仕様の形が見えやすくなります。

```csharp
abstract record StatusScreenState;

record Loading()
  : StatusScreenState;

record Loaded(MemberVm SelectedMember)
  : StatusScreenState;

record Error(string Message)
  : StatusScreenState;
```

</div>

<div class="p-5 border border-emerald-500/40 rounded-xl bg-emerald-500/10">

## 表現しにくくなる状態

```text
LoadingなのにMemberが選択されている
Errorなのに通常操作が有効
Loadedなのに表示対象がない
```

</div>

</div>

<!--
- ViewModelを型として設計する例
- Loading、Loaded、Errorなどを状態として分ける
- 仕様上ありえない状態を作りにくくする
- MVVMの宣言性はこういう設計と相性がよい
-->

---
layout: center
class: text-center
---

# ここまでは<br><span class="text-emerald-400">Presentation State</span>の話

<div class="pt-8 text-xl opacity-80">
ViewModelが表すのは、Viewの仕様上取りうる論理状態
</div>

<!--
- ここまでの整理
- ViewModelはPresentation Stateを表す
- ViewはViewModelの状態を投影する
- 次からゲーム特有のずれを見る
-->

---
layout: default
---

# ゲームでは「現在」がずれる

例：ソシャゲの限界突破演出。

<div class="grid grid-cols-2 gap-6">

<div>

```text
ユーザーが「限界突破」ボタンを押す
        ↓
API成功。Model層では 2凸 → 3凸 が確定
        ↓
ViewModelへ即時反映
        ↓ binding
Viewも即座に3凸表示になる
```

<div class="p-3 border border-red-500/40 rounded-xl bg-red-500/10 mt-3 text-sm">

Model上の値としては正しい。  
しかしPresentation上のタイミングとしては早すぎる。

</div>

</div>

<div>
  <video src="/videos/limit_break_demo.mov" autoplay loop muted playsinline class="rounded-xl border border-white/10 shadow-lg w-full" />
  <div class="text-xs text-gray-400 mt-2 text-center">※画面右側に注目</div>
</div>

</div>

<!--
- Modelでは結果が確定している
- Presentationではまだ旧状態から演出を始めたい
- Modelの現在とPresentationの現在がずれる
- Bindingは期待通り動いている
- 問題は最新値をViewModelへ適用するタイミング
-->

---
layout: default
---

# 問題はBindingではなく、適用タイミング

```text
Model change
    ↓
ViewModel change
    ↓ binding
View change
```

<br>

この流れ自体は自然で便利です。  
問題になるのは、**Modelの最新値をViewModelへ常時即時反映する設計**です。

<br>

```text
Model change
    ↓
ViewModel change   ← Presentationとしてはまだ早い
    ↓ binding
View change        ← 結果が見えてしまう
```

<!--
- Bindingそのものを悪者にしない
- ViewModelが変わればViewが変わるのはMVVMの便利な性質
- Model変更と同時にVMを変えると、演出時間を挟めない
- VMはModelのライブミラーではない
-->

---
layout: center
class: text-center
---

# ViewModelは<br>「今見せている状態」を表してよい

<div class="pt-8 text-xl opacity-80">
Modelの最新値ではなく、Presentationの現在を表す
</div>

<!--
- Modelではすでに3凸
- Presentationではまだ2凸として見せる瞬間がある
- そのときViewModelが2凸を持つのは不正ではない
- ViewModelはPresentation Stateだから
- 前半の定義がここで効く
-->

---
layout: default
---

# 反映タイミングをViewModelの外側で制御する

View ↔ ViewModel のbindingは維持してよい。<br>
制御すべきなのは、**Modelの結果をいつViewModelへ適用するか**です。

<br>

```csharp
// Model側では、ここで結果が確定する
var result = await useCase.LimitBreakAsync();

// 表示上は、旧状態のまま演出する
await presentation.PlayLimitBreakAsync(result);

// 結果を見せるタイミングで、ViewModelへ適用する
viewModel.Apply(result);
```

<br>

```text
Model側:   2凸 ── API成功 → 3凸 ─────────
表示上:    2凸 ───── 演出 ── 結果開示 → 3凸
VM:        2凸 ───────────── Apply() ─→ 3凸
```

<!--
- ViewとViewModelの関係は維持できる
- 調整するのはModel結果をViewModelへ反映するタイミング
- UseCase完了時点ではModel側の結果確定
- Presentation側は旧状態のまま演出
- 結果開示時点でViewModelへ適用
-->

---
layout: center
class: text-center
---

# ここからは<br>Presentationだけでは説明しにくい領域

<div class="pt-8 text-xl opacity-80">
状態を「見せる」だけではなく、<br>次の状態を「作る」ものがある
</div>

<!--
- ここで話を切り替える
- ここまではPresentation Stateと反映タイミングの話
- 次はViewModelの投影として扱いにくいもの
- ゲーム世界の次状態を作る領域を見る
-->

---
layout: default
---

# この発表での「Simulation」

ここでは便宜上、次の領域を **Simulation** と呼びます。

<br>

<div class="p-6 border border-amber-500/40 rounded-xl bg-amber-500/10">

## 現在のゲーム世界の状態と入力から、
## 次のゲーム世界の状態を作る領域

```text
state(t) + input → state(t+1)
```

</div>

<br>

<div class="text-sm opacity-80">
MVVMの標準用語ではなく、Model / Presentation だけでは説明しにくい状態空間を分けるための呼び方です。
</div>

<!--
- Simulationは独自の補助概念
- MVVM標準用語ではない
- 定義：現在のゲーム世界の状態と入力から、次のゲーム世界の状態を作る領域
- 例：Transform、Velocity、Collider、接地状態、移動入力
- 後半の状態空間を整理するための名前
-->

---
layout: default
---

# 表示されるものが、次の状態を作っている

探索中の3Dプレイヤーを考えます。

<br>

```text
Lスティック入力
      ↓
移動方向を計算
      ↓
CharacterController / Rigidbody / NavMeshAgent
      ↓
Transform.position が変わる
      ↓
敵との距離、会話可能距離、クエスト到達判定が変わる
```

<br>

このGameObjectは、表示結果であるだけではありません。<br>
**ゲーム世界の次の状態を作っています。**

<!--
- 探索中の3Dプレイヤーの例
- 画面に表示されるのでPresentationの一部でもある
- ただし入力を受けて移動する
- Transformが他の判定に影響する
- ViewModelの状態を見た目にしているだけではない
- Simulationにも参加している
-->

---
layout: center
class: text-center
---

# 投影か、状態遷移か

<br>

```text
Presentation:
  state → appearance

Simulation:
  state(t) + input → state(t+1)
```

<!--
- Presentation：状態を見た目へ変換する
- Simulation：現在の状態と入力から次の状態を作る
- 探索中のプレイヤーは後者の役割を持つ
- 画面に映るかどうかではなく、責務で見る
-->

---
layout: default
---

# 同じ3Dキャラクターでも、文脈で変わる

<div class="text-sm opacity-90 mb-3">
見るべきなのは、<b>ゲーム状態の遷移に参加しているか、決定済みの状態を表現しているか</b>です。
</div>

<div class="grid grid-cols-2 gap-4">

<div class="p-3 border border-red-500/30 rounded-xl bg-red-500/5 flex flex-col justify-between">

<div>
  <h2 class="text-base font-bold text-red-300">探索中のプレイヤー</h2>
  <div class="text-xs text-gray-300 mt-0.5 mb-2">
    PlayerActorが移動 → Transformが変化 → ゲーム状態が変わる
  </div>
</div>

<img src="/images/player_exploration.png" class="rounded-lg border border-red-500/20 shadow w-full aspect-video object-contain bg-black/40" alt="Simulation Actor" />

<div class="text-xs text-red-200 font-semibold mt-2">
▶ Simulation Actor と見る方が自然
</div>

</div>

<div class="p-3 border border-emerald-500/30 rounded-xl bg-emerald-500/5 flex flex-col justify-between">

<div>
  <h2 class="text-base font-bold text-emerald-300">ターン制バトルの結果表示</h2>
  <div class="text-xs text-gray-300 mt-0.5 mb-2">
    Battle Modelで結果を決定 → 3Dキャラが見せる
  </div>
</div>

<img src="/images/battle_presentation.png" class="rounded-lg border border-emerald-500/20 shadow w-full aspect-video object-contain bg-black/40" alt="View" />

<div class="text-xs text-emerald-200 font-semibold mt-2">
▶ View として扱いやすい
</div>

</div>

</div>

<!--
- 同じ3Dキャラクターでも文脈で役割が変わる
- 探索中：Transformの変化がゲーム状態を変える
- ターン制バトル：結果が先に決まり、3Dキャラが見せる
- 3Dかどうかではなく、状態遷移に参加しているかを見る
-->

---
layout: default
---

# 特定NPCへの接近条件で境界が見える

<div class="grid grid-cols-2 gap-6 items-center">

<div>

仕様：クエストNPCの一定距離以内に近づいたら進行。

```text
Simulation（位置の観測）
  Transform.position = (127.3, 2.0, -83.5)
        ↓
Simulation（空間上の解釈）
  IsWithinRange(QuestNpc) == true
        ↓ 意味に変換する
Quest / Model側の解釈
  ApproachedNpc(QuestNpc)
        ↓
Quest condition satisfied
```

<div class="text-xs opacity-85 mt-2">
Quest側は「近づいたら進行する」ルールを扱えるが、TransformやColliderを自前で観測するわけではない。
</div>

</div>

<div>
  <video src="/videos/quest_area_trigger.mp4" autoplay loop muted playsinline class="rounded-xl border border-white/10 shadow-lg w-full" />
</div>

</div>

<!--
- NPC接近条件の例
- 実際に位置を観測するのはSimulation側
- TransformやColliderから空間上の出来事を検出する
- Model側には「QuestNpcに近づいた」という意味を渡す
- Quest側がTransformやColliderを直接見続ける必要はない
-->

---
layout: center
class: text-center
---

<div class="text-2xl font-bold leading-relaxed">
Simulationは空間上の出来事を検出する<br>
<span class="opacity-90">Modelはそれをゲーム上の事実として解釈する</span>
</div>

<!--
- Simulation：空間上の出来事を検出する
- Model：それをゲーム上の事実として解釈する
- Transform.positionをQuestロジックへ直接持ち込まない
- Questが欲しいものは「QuestNpcに近づいた」という意味のある事実
-->

---
layout: default
---

# ゲームには複数の状態空間がある

「ModelかViewか」だけでは、ゲームを説明しきれません。

<br>

```text
Model State
  所持金、アイテム、キャラの凸段階、クエスト進行

World Simulation State
  Transform、Velocity、Collider、接地状態、移動入力

Presentation State
  選択中タブ、表示中の値、演出フェーズ、カメラ、フェード
```

<br>

これらはすべて「状態」ですが、<br>
**意味・寿命・更新タイミング・何を正とするかが違います。**

<!--
- ここまでの話を三つの状態空間として整理する
- Model State
- World Simulation State
- Presentation State
- すべて状態だが、同じ種類ではない
- 意味、寿命、更新頻度、何を正とするかが違う
-->

---
layout: center
class: text-center
---

# ゲームには<br><span class="text-amber-400">「現在」</span>が複数ある

<div class="pt-8 text-xl opacity-80">
Modelの現在 / Simulationの現在 / Presentationの現在
</div>

<!--
- 三つの現在が常に一致するとは限らない
- Modelでは結果が確定している
- Simulationではフレームごとに状態が進む
- Presentationでは演出上の現在がある
- それぞれ別の意味で正しい
-->

---
layout: default
---

# では、MVVMはどこで使うのか

<div class="grid grid-cols-2 gap-6">

<div class="p-5 border border-emerald-500/40 rounded-xl bg-emerald-500/10">

## MVVMで扱いやすい

- 設定画面
- ショップ
- インベントリ
- ステータス画面
- HUDの一部
- ターン制バトルのUI / 結果表示

</div>

<div class="p-5 border border-amber-500/40 rounded-xl bg-amber-500/10">

## 境界を明示したい

- Model結果をいつViewModelへ反映するか
- 演出中にどのPresentation Stateを持つか
- Simulationの出来事をどうModelへ渡すか
- ViewModelが担当する状態空間はどこまでか

</div>

</div>

<br>

<div class="p-4 border border-red-500/40 rounded-xl bg-red-500/10">

入力で動く3Dプレイヤー、Physics / Collision、Transformが判定に関わる領域は、Simulationとして分けた方が扱いやすい。

</div>

<!--
- MVVMが得意な領域：Presentation StateをViewModelとして表せるところ
- 境界が必要な領域：反映タイミング、演出中の状態、SimulationからModelへの意味変換
- SimulationそのものをViewModelに押し込まない
- MVVMを使わないというより、担当範囲を切る
-->

---
layout: default
---

# 判断基準

<div class="p-6 border-2 border-amber-500/50 rounded-xl bg-amber-500/10 text-center my-4">
  <div class="text-xl font-bold leading-relaxed">
    その状態は、<span class="text-emerald-400">Viewの仕様上取りうる論理状態</span>か。<br>
    それとも、<span class="text-red-400">ゲーム世界の次状態を作る状態</span>か。
  </div>
</div>

<br>

- ViewModelはModelのライブミラーではない
- ViewModelは「今ユーザーに提示している状態」を表してよい
- ViewModelが強いのは、Presentation Stateを型で表せる範囲
- SimulationまでViewModelの投影として扱うと境界が崩れやすい

<!--
- 実務上の判断基準
- ViewModelに置くべき状態かを見る
- Viewの仕様上取りうる論理状態ならViewModelに向く
- ゲーム世界の次状態を作るならSimulationとして分ける
- Modelの最新値をいつ反映するかも明示する
-->

---
layout: center
class: text-center
---

# MVVMを活かすには

## ViewModelを<br><span class="text-emerald-400">Presentationの状態空間</span>として設計する

<div class="pt-8 text-xl opacity-80">
Model / Simulation / Presentation の現在を混ぜない
</div>

<!--
- 結論
- MVVMの強みはPresentationを宣言的な状態として扱えること
- ViewModelはViewの仕様上取りうる状態を表す
- Modelの最新状態を常に同期する箱ではない
- SimulationをViewModelに押し込まない
- 状態空間を分けることでMVVMを活かせる
-->

---
layout: center
class: text-center
---

# ご清聴ありがとうございました

ご質問があればお願いします

<!--
- MVVMの強み：Presentation Stateを宣言的に表せる
- ゲームでの注意点：Model、Simulation、Presentationの現在がずれる
- ViewModelに置く状態と、Simulationとして分ける状態を切り分ける
-->
