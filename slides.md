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


<!--
今日は「MVVMはなぜゲームに向かないと言われがちなのか」という話をします。

先に方向だけ言うと、MVVM自体を否定する話ではありません。
ゲームでは、MVVMがきれいに成立する前提が崩れやすい場面がある、という話です。

特に今日は、Domain / Simulation / Presentation という三つの状態の世界を区別すると、なぜそう見えるのかを考えます。
-->

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


<!--
結論から入ります。

MVVMがきれいに働くのは、Presentationの論理状態をViewModelに置いて、Viewをその結果として扱えるときです。

たとえば「選択中のタブが2番」「HPが危険域」といった状態をViewModelに置き、Viewはそれをどう見せるかだけを担当する。これは非常に素直です。

ゲームで難しいのは、この前提が壊れる場面が多いことです。
一つはModelの現在とPresentationの現在がズレること。もう一つは、画面に見えているオブジェクト自身がゲーム状態を変えることです。
-->

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


<!--
最初にViewModelをどう捉えるかだけ整理します。

MVVMというとData BindingやReactivePropertyを思い浮かべがちですが、それは接続方法です。
ViewがInitializeでViewModelを受け取って自分でSubscribeしてもいいし、変化しない画面ならimmutableな値を一度渡すだけでも構いません。

大事なのは、ViewModelが「その画面にとって意味のある状態」を表していることです。

HPの例なら、Domain上の23/100という値から、Presentation上は0.23という割合やIsDangerという意味を作れる。
逆に、赤くする・点滅させるといった具体的な見せ方まではView側に残せます。
-->

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


<!--
ViewModelはDomainのコピーではありません。

たとえばパーティー画面で、Alice・Bob・Carolがメンバーであることはゲーム世界の事実です。
でも「今Bobのタブを開いている」は、ゲーム世界には存在しません。これはPresentationだけの状態です。

このSelectedMemberIndexをViewModelが持ち、Viewはそれに従って表示する。
こういう領域では、ViewをViewModelの投影として扱いやすく、MVVMは非常に素直に機能します。
-->

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


<!--
ここからゲーム特有の話に入ります。まずは演出の時間です。

限界突破のような処理を考えます。ボタンを押してAPIが成功した時点で、Model層ではもう2凸から3凸に更新されている。
でもユーザーには、まず暗転して、演出して、結果を見せる瞬間で3凸を開示したい。

ModelをViewModelへ常時即時同期していると、フェード前に一瞬だけ3凸が見える、という事故が起こります。

ここで重要なのは「値が間違っている」のではないことです。
値は正しい。でもPresentationの時間としては早すぎる。
-->

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


<!--
ここでは、ModelとPresentationでcommitのタイミングを分けます。

ViewとViewModelのbindingを捨てる必要はありません。制御したいのは、Modelの結果をいつViewModelへ反映するかです。

[click] まずUseCaseが完了して、Domain / Model側では結果が確定します。ここでは3凸になっている。

[click] ただしPresentationでは旧状態のまま演出を再生します。

[click] 結果を見せるrevealポイントに来たら、そこで初めてViewModelへ適用します。

[click] するとViewはいつも通りViewModelに従って3凸表示へ変わる。

つまりViewModelはModelのライブミラーではなく、「今ユーザーに何を提示しているか」を表すものだ、と捉えると自然です。
-->

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


<!--
次の壁は、リアルタイムに動く3Dオブジェクトです。

探索中のプレイヤーは、画面に映っているので一見Viewに見えます。
でも実際には、入力を受けて移動し、そのTransformが敵との距離や会話判定、クエスト到達判定に影響します。

つまりこのGameObjectは「決まった状態を描画しているだけ」ではありません。
自分自身がゲーム世界の次の状態を作っています。

ここでは、ViewというよりSimulation Actorと考えた方が責務に合います。
-->

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


<!--
ただし、3DだからViewではない、という話でもありません。

探索中のプレイヤーでは、Transformの変化そのものがゲーム状態を変えます。だからSimulation寄りです。

一方、ターン制コマンドバトルなら、Battle Model側で誰が誰に攻撃して何ダメージ、という結果が先に決まっている場合があります。
その後で3Dキャラが走って、剣を振って、ダメージを演出する。

この場合、3Dキャラクターは「決定済みのゲーム状態を見せる側」なので、かなりView / Presentation Actorとして扱いやすい。

要するに、見た目が3Dかどうかではなく、そのオブジェクトがゲーム状態の原因なのか、結果なのかを見るべきです。
-->

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


<!--
ここまでの二つの例をまとめると、ゲームをModelとViewの二つだけで考えるのが苦しい理由が見えてきます。

少なくとも、永続的なゲームルールやアプリケーション状態、毎フレーム動くWorld Simulation、そしてユーザーにどう見せるかというPresentationがあります。

これらは全部「状態」ですが、同じ種類の状態ではありません。
寿命も更新頻度も、誰が正とするかも違います。

MVVMの問題というより、異なる状態空間を全部ひとつの同期モデルで扱おうとすると苦しくなる、というのがここでのポイントです。
-->

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


<!--
この境界が分かりやすく出るのが、地点到達型のクエストです。

仕様としては「神殿入口の一定距離内に入ったら進行」。
実際に位置を観測するのはTransformやColliderを持つSimulation側です。
そこで「TempleEntranceの範囲内にいる」という空間的な意味に変換し、さらにQuest側では「TempleEntranceに到達した」というドメイン上の事実として扱う。

Domainは「到達したら進行する」というルールを知ることはできます。
でも、ColliderやTransformを自分自身で観測する必要はありません。

このように、ゲームでは状態そのものだけでなく、状態をどこで観測し、どこで意味づけするかという境界が重要になります。
-->

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


<!--
最後にまとめます。

MVVMが向いているのは、Presentation StateをViewModelとして表し、Viewをその投影として扱える問題です。
設定画面、ショップ、インベントリ、ステータス画面などはかなりこの形にしやすい。

一方ゲームでは、ModelとPresentationで時間がズレたり、画面に見えているオブジェクト自身がSimulationの状態遷移に参加したりします。

なので「ゲームにMVVMは向かない」と一括りにするより、どこまでがPresentationで、どこからがSimulationなのかを見る方が有用です。

一番短く言えば、MVVMが得意なのは状態をどう見せるか。ゲームが難しいのは、見えているもの自身もゲーム状態を変えることです。
-->

---
layout: center
class: text-center
---

# ご清聴ありがとうございました

議論・ツッコミ歓迎です

<!--
以上です。

「そこはViewModelではなくPresentation Modelでは？」とか、「このケースなら別の切り方がある」といったツッコミも含めて、ぜひ議論したいです。
-->

