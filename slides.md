---
theme: default
background: https://cover.sli.dev
title: MVVMはなぜゲームに向かないと言われがちなのか
info: |
  ## MVVMはなぜゲームに向かないと言われがちなのか
  ViewModelで扱える状態、扱いにくい状態
class: text-center
drawings:
  persist: false
transition: slide-left
mdc: true
---

# MVVMはなぜゲームに<br><span class="text-red-400">向かない</span>と言われがちなのか

## ViewModelで扱える状態、扱いにくい状態

<div class="pt-8 text-sm opacity-60">
Domain / Simulation / Presentation の境界から考える
</div>

---
layout: default
---

# 先に結論

MVVMそのものがゲームに向かない、という話ではありません。

<br>

<div class="p-6 border border-emerald-500/40 rounded-xl bg-emerald-500/10">

## MVVMがきれいに働く条件

```text
Presentationの論理状態をViewModelに置ける
        ↓
Viewを、その状態の投影として扱える
```

</div>

<br>

ゲームでは、この前提が崩れやすい場面があります。

- Modelの現在と、Presentationの現在が一致しない
- 画面に出ているオブジェクト自身が、ゲーム状態を変えている

---
layout: default
---

# ViewModelとは何か

ViewModelは、Viewのピクセルや描画APIではなく、<br>
**その画面にとって意味のある状態**を表すものです。

<br>

```text
Model / Application
  PlayerHp = 23 / 100
        │
        ▼  presentation向けに解釈する
ViewModel
  HpRate = 0.23
  IsDanger = true
        │
        ▼  具体的に表示する
View
  ゲージ幅を23%にする
  危険状態として強調する
```

<br>

Data Binding / Rx / Command は、この接続を実装する手段です。<br>
それ自体がMVVMの本体ではありません。

---
layout: default
---

# Presentationにしかない状態

例：パーティーステータス画面。

<br>

```text
Domain / Model
  PartyMembers = [Alice, Bob, Carol]

        ↓  画面で誰を見ているかは、Domainには存在しない

ViewModel
  SelectedMemberIndex = 1
  SelectedMember = Bob

        ↓

View
  Bobのステータスを表示
  Bobのタブを選択状態にする
```

<br>

<div class="p-4 border border-emerald-500/40 rounded-xl bg-emerald-500/10">

**「今Bobを見ている」はPresentationの状態です。**  
このような状態をViewModelに置ける領域では、MVVMは素直に機能します。

</div>

---
layout: default
---

# 壁1：Presentationには独自の時間がある

例：ソーシャルRPGの限界突破演出。

<br>

```text
ユーザーが「限界突破」ボタンを押す
        ↓
API成功。Model層では 2凸 → 3凸 が確定
        ↓
でも画面では、まだ2凸の状態から演出を始めたい
        ↓
演出のrevealタイミングで、はじめて3凸を見せたい
```

<br>

ここでModelの更新をViewModelへ即時反映すると、<br>
**演出前に結果だけが一瞬表示される**ことがあります。

<br>

> 値としては正しい。しかし、見せるタイミングとしては正しくない。

---
layout: default
---

# ModelのcommitとPresentationのcommitを分ける

View ↔ ViewModel のbindingは維持してよい。<br>
制御すべきなのは、**Modelの最新状態をいつViewModelへ適用するか**です。

<br>

```csharp {all|1|3|5|all}
// Domain / Model 側では、ここで結果が確定する
var result = await useCase.LimitBreakAsync();

// Presentation上は、まだ旧状態を見せたまま演出する
await presentation.PlayLimitBreakAsync(result);

// reveal後に、Presentationの現在として適用する
viewModel.Apply(result);
```

<br>

```text
Model time:        API成功 ───────────── 3凸
Presentation time: 2凸 ── 演出 ── reveal ── 3凸
```

ViewModelは「Modelのライブミラー」ではなく、<br>
**今ユーザーに提示している状態**を表します。

---
layout: default
---

# 壁2：3Dプレイヤーは単なるViewではない

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

<br>

```text
View:        state → appearance
Simulation: state(t) + input → state(t+1)
```

---
layout: default
---

# 同じ3Dキャラクターでも、文脈で変わる

3DだからViewではない、という話ではありません。<br>
重要なのは、**ゲーム状態を決定しているか、決定済みの状態を表現しているか**です。

<br>

<div class="grid grid-cols-2 gap-6">

<div class="p-4 border border-red-500/30 rounded-xl bg-red-500/5">

## 探索中のプレイヤー

```text
PlayerActorが動く
      ↓
Transformが変わる
      ↓
ゲーム状態が変わる
```

Simulation Actor と見る方が自然。

</div>

<div class="p-4 border border-emerald-500/30 rounded-xl bg-emerald-500/5">

## ターン制バトルの演出

```text
Battle Modelが結果を決める
      ↓
3Dキャラが攻撃を演出する
```

Presentation Actor / View として扱いやすい。

</div>

</div>

---
layout: default
---

# ここで抽象化する：ゲームには複数の状態空間がある

「ModelかViewか」だけでは、ゲームを説明しきれません。

<br>

```text
Domain / Application State
  所持金、アイテム、キャラの凸段階、クエスト進行

World Simulation State
  Transform、Velocity、Collider、接地状態、移動入力

Presentation State
  選択中タブ、表示中の値、演出フェーズ、カメラ、フェード
```

<br>

これらはすべて「状態」ですが、<br>
**意味・寿命・更新タイミング・authority が違います。**

---
layout: default
---

# クエスト到達条件で境界が見える

仕様：神殿の入口から一定距離内に到達したらクエスト進行。

<br>

```text
Observation / Simulation
  Transform.position = (127.3, 2.0, -83.5)
        ↓
Spatial interpretation / Simulation
  IsInsideArea(TempleEntrance) == true
        ↓ semantic boundary
Domain interpretation / Quest
  ReachedLocation(TempleEntrance)
        ↓
Quest condition satisfied
```

<br>

Domainは「到達したら進行する」というルールを扱えます。<br>
しかし、TransformやColliderを自前で観測するわけではありません。

---
layout: default
---

# まとめ：一番短い答え

<br>

<div class="p-6 border-2 border-amber-500/50 rounded-xl bg-amber-500/10 text-center my-4">
  <div class="text-xl font-bold leading-relaxed">
    MVVMが得意なのは、<span class="text-emerald-400">Presentation StateをViewModelで表すこと</span>。<br>
    ゲームが難しいのは、<span class="text-red-400">表示されているもの自身が状態遷移に参加すること</span>。
  </div>
</div>

<br>

- ViewModelはModelのライブミラーではない
- 3Dオブジェクトは、ViewではなくSimulation Actorであることがある
- ゲームでは Domain / Simulation / Presentation の境界を見る必要がある
- MVVMは、ViewをViewModelの投影として扱える範囲で使うと強い

---
layout: center
class: text-center
---

# ご清聴ありがとうございました

議論・ツッコミ歓迎です
