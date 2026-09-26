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
ゲームにおける Domain / Simulation / Presentation の境界から考える
</div>

---
layout: default
---

# 今日の結論

MVVMがゲームに向かない、というより、<br>
**MVVMがきれいに成立する前提が、ゲームでは崩れやすい**。

<br>

<div class="p-5 border border-emerald-500/40 rounded-xl bg-emerald-500/10">

## MVVMが得意な形

```text
Presentation State を ViewModel に置く
        ↓
View はそれを具体的な表示へ写す
```

</div>

<br>

<div class="p-5 border border-red-500/40 rounded-xl bg-red-500/10">

## ゲームで崩れやすい点

- 表示されているオブジェクト自身が、状態を持って時間発展する
- Modelの現在とPresentationの現在が一致しないことがある

</div>

---
layout: default
---

# 前提：MVVM = データバインディングではない

Data Binding / Rx / Command は、View と ViewModel を接続するための実装手段です。

<br>

<div class="grid grid-cols-2 gap-6 pt-2">

<div class="p-4 border border-blue-500/30 rounded-xl bg-blue-500/5">

## MVVMの関心

- Viewから表示上の判断を分離する
- ViewModelにPresentationの論理状態を置く
- Viewはその状態を具体的な表示へ落とす

</div>

<div class="p-4 border border-amber-500/30 rounded-xl bg-amber-500/5">

## Bindingの関心

- 値の変更をどうViewへ伝えるか
- UIイベントをどうViewModelへ渡すか
- 購読・解除・寿命をどう管理するか

</div>

</div>

<br>

> ReactivePropertyを使っているかどうかは、MVVMの本質ではない。

---
layout: default
---

# ViewModelとは何か

ViewModelは、Viewのピクセルや描画APIではなく、<br>
**その画面にとって意味のあるPresentation Stateをモデル化する**。

<br>

```text
[ Model / Application ]
    PlayerHp = 23 / 100
          │
          ▼  presentation向けに解釈する
[ ViewModel ]
    HpRate = 0.23
    IsDanger = true
          │
          ▼  具体的に表示する
[ View ]
    ゲージ幅を23%にする
    危険状態として強調する
```

<br>

- `HpRate` や `IsDanger` は、ViewModelに置きやすい
- 色・点滅・マテリアル切り替えは、View側の具体表現として扱いやすい

---
layout: default
---

# M と VM/V の間には境界がある

MVVMを単なる三段変換として見ると、少し誤解しやすい。

<br>

```text
Model / Application
  サーバー状態のローカルコピー、UseCase、Repository、Domain Logic など

──────────────────── boundary

Presentation
  ViewModel  = 今ユーザーに提示する論理状態
  View       = その具体的な表示
```

<br>

ViewModelはModelのミラーではありません。<br>
**Modelを材料にしつつ、Presentationの現在を表すためのモデル**です。

---
layout: two-cols
---

# Presentationにしかない状態

例：パーティーステータス画面

```text
Domain / Model
  PartyMembers = [Alice, Bob, Carol]
```

これはゲーム世界の事実です。

<br>

```text
Presentation
  SelectedMemberIndex = 1
```

これは「いまBobのタブを見ている」という、画面上の状態です。

::right::

<div class="pl-4 pt-8">

<div class="p-4 border border-emerald-500/30 rounded-xl bg-emerald-500/10">

## ここではMVVMがよく効く

```text
SelectedMemberIndex
        ↓
SelectedMember
        ↓
表示内容・選択タブ
```

ViewをViewModelの投影として扱いやすい。

</div>

<br>

<div class="text-sm opacity-80">
このスコープでは、ViewModelを<br>
「presentation state の基準表現」と見なせる。
</div>

</div>

---
layout: default
---

# ただし、ゲームには「演出の時間」がある

例：ソーシャルRPGの限界突破演出。

<br>

```text
ユーザーが「限界突破」ボタンを押す
        ↓
API成功。Model層では 2凸 → 3凸 が確定
        ↓
でもPresentationでは、まだ2凸の画面から演出を始めたい
        ↓
演出のrevealタイミングで、はじめて3凸を見せたい
```

<br>

ここでModelの更新をViewModelへ即時反映すると、<br>
**演出前に結果だけが一瞬表示される**。

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

ViewModelは「Modelの最新値」ではなく、<br>
**今ユーザーに提示している状態**を表す。

---
layout: default
---

# インゲームでは、Viewが単なるViewではない

探索中の3Dプレイヤーを考える。

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
**ゲーム世界の次の状態を作っている**。

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

## ターン制バトルの3D演出

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

# ゲームには複数の状態空間がある

「ModelかViewか」だけでは、ゲームを説明しきれません。

<br>

```text
Remote / Domain State
  所持金、アイテム、キャラの凸段階、クエスト進行

World Simulation State
  Transform、Velocity、Collider、接地状態、移動入力

Presentation State
  選択中タブ、表示中の値、演出フェーズ、カメラ、フェード
```

<br>

これらはすべて「状態」ですが、<br>
**意味・寿命・更新タイミング・authority が違う**。

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

Domainは「到達したら進行する」というルールを扱える。<br>
しかし、TransformやColliderを自前で観測するわけではない。

---
layout: default
---

# オンラインなら、authorityも分かれる

クライアントがCollider侵入を観測したとしても、<br>
サーバーから見ればそれはまだ **claim** です。

<br>

```text
Client Simulation
  EnteredArea(TempleEntrance)
        ↓
Client Application
  現在のクエストに関係ありそうならAPIを呼ぶ
        ↓
Server Application / Domain
  現在の進行状況・条件・妥当性を確認して確定する
```

<br>

- Client側判定：APIを呼ぶかどうかのprefilter
- Server側判定：ゲーム状態を進めてよいかのauthoritativeな判断

同じ条件を見ていても、責務は同じではない。

---
layout: default
---

# MVVMが向く場所・注意が必要な場所

<div class="grid grid-cols-2 gap-6">

<div class="p-4 border-2 border-emerald-500/50 rounded-xl bg-emerald-500/5">

## 向きやすい領域

- 設定
- ショップ
- インベントリ
- ステータス画面
- ターン制バトルのUIや演出制御の一部

<br>

ViewをViewModelの投影として扱いやすい。

</div>

<div class="p-4 border-2 border-amber-500/50 rounded-xl bg-amber-500/5">

## 注意が必要な領域

- 探索中の3Dプレイヤー
- Physics / Navigation
- Colliderによる進行判定
- カットシーンや結果開示のタイミング

<br>

SimulationやPresentation timeを無視して同期すると壊れやすい。

</div>

</div>

---
layout: default
---

# まとめ

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
