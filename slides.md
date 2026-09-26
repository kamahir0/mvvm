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

結論から言うと、MVVMそのものを否定する話ではありません。
むしろ、MVVMがきれいにハマる場所と、苦しくなる場所を分けて考えたい、という話です。
-->

---
layout: center
class: text-center
---

# 「MVVMはゲームに向かない」

## ……本当に？

<!--
まず、よくある言い方として「MVVMはゲームに向かない」があります。
でもこれは、ちょっと雑な言い方だと思っています。

ゲーム内の設定画面、ショップ、インベントリ、ステータス画面には普通にハマることがあります。
では、どこから苦しくなるのか。それを考えるのが今日の話です。
-->

---
layout: default
---

# 今日の結論

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

- Modelの「今」と、Presentationの「今」が一致しない
- 画面に出ているオブジェクト自身が、ゲーム状態を変えている

<!--
MVVMがきれいに働くのは、Presentationの論理状態をViewModelに置いて、Viewをその投影として扱えるときです。

「今どのタブを選んでいるか」「HPが危険域か」といった状態をViewModelに置き、Viewはそれをどう見せるかだけを担当する。これは素直です。

ゲームで難しいのは、この前提が壊れる場面が多いことです。
-->

---
layout: default
---

# まず：ViewModelとは何か

ViewModelは、Viewのピクセルや描画APIではなく、<br>
**その画面にとって意味のある論理状態**を表すものです。

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

ViewModelは、Presentationのために意味を与える層です。

<!--
最初にViewModelをどう捉えるかを整理します。

ここではViewModelを、「その画面にとって意味のある論理状態」と捉えます。

HPの例なら、Model上の23/100という値から、Presentation上は0.23という割合やIsDangerという意味を作れる。
逆に、赤くする、点滅させる、といった具体的な見せ方まではView側に残せます。
-->

---
layout: center
class: text-center
---

# ViewModelは<br><span class="text-red-400">Modelの鏡</span>ではない

<div class="pt-8 text-xl opacity-80">
ViewModelは、Presentationの状態モデルである
</div>

<!--
ここでまず、一つ目のキーワードです。
ViewModelはModelの鏡ではありません。

Modelの値をただ横流しするだけなら、それはViewModelというより単なるコピーです。
今日の話では、ViewModelをPresentationの状態モデルとして捉えます。
-->

---
layout: default
---

# ViewModelは「変更通知するオブジェクト」なのか？

ステータス画面のように、初期化時点で表示が決まる画面を考えます。

<br>

<div class="grid grid-cols-2 gap-6">

<div class="p-4 border border-emerald-500/30 rounded-xl bg-emerald-500/5">

## immutableなVM

```csharp
readonly record struct StatusVm(
    int CurrentHp,
    int MaxHp)
{
    public float HpRate =>
        (float)CurrentHp / MaxHp;
}
```

</div>

<div class="p-4 border border-blue-500/30 rounded-xl bg-blue-500/5">

## Viewが受け取って反映

```csharp
void Initialize(StatusVm vm)
{
    hpText.text =
        $"{vm.CurrentHp}/{vm.MaxHp}";

    hpGauge.fillAmount = vm.HpRate;
}
```

</div>

</div>

<br>

<div class="p-4 border border-amber-500/40 rounded-xl bg-amber-500/10">

**「変わらない状態」をReactiveにする必要はない。**

</div>

<!--
ViewModelというと、ReactivePropertyを持っていて、ViewがSubscribeする形を想像しがちです。

でもそれは実装方式の一つです。

ステータス画面のように、開いた瞬間に表示内容が決まり、その後ユーザー操作で変化しない画面なら、ViewModelはreadonlyな値型でも構いません。

私はこれもMVVM的に捉えます。なぜなら、その画面にとって意味のあるPresentation状態をViewModelとして切り出し、Viewがそれを具体的な表示にしているからです。

ただし、ここで宗派戦争をしたいわけではありません。大事なのは、MVVMを自動同期技術ではなく、Presentation Stateのモデル化として捉えることです。
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

**「今Bobを見ている」は、ゲーム世界の事実ではない。**  
それはPresentationの状態です。

</div>

<!--
ViewModelはDomainのコピーではありません。

Alice、Bob、Carolがパーティにいることはゲーム世界の事実です。
でも、今Bobのタブを開いている、はゲーム世界の事実ではありません。

これはPresentationにしかない状態です。

このSelectedMemberIndexをViewModelが持ち、Viewはそれに従って表示する。
こういう領域では、ViewをViewModelの投影として扱いやすく、MVVMは非常に素直に機能します。
-->

---
layout: center
class: text-center
---

# ViewはViewModelの投影になる

<div class="pt-8 text-2xl opacity-80">
ここまでは、きれい。
</div>

<!--
ここまではかなりきれいです。
ViewModelがPresentationの論理状態を持ち、Viewはそれを具体的に見せる。

この範囲ではMVVMはかなり気持ちよく使えます。

ここから、ゲームで壁に当たる例を見ていきます。
-->

---
layout: default
---

# 壁1：正しい値なのに、表示するとバグになる

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

Modelの更新をViewModelへ即時反映すると、<br>
**演出前に結果だけが一瞬表示される**ことがあります。

<br>

> 値としては正しい。しかし、見せるタイミングとしては正しくない。

<!--
ここからゲーム特有の話に入ります。まずは演出の時間です。

限界突破のような処理を考えます。
ボタンを押してAPIが成功した時点で、Model層ではもう2凸から3凸に更新されています。

でもユーザーには、まず暗転して、演出して、結果を見せる瞬間で3凸を開示したい。

ModelをViewModelへ常時即時同期していると、フェード前に一瞬だけ3凸が見える、という事故が起こります。

ここで重要なのは値が間違っているのではないことです。
値は正しい。でもPresentationの時間としては早すぎる。
-->

---
layout: center
class: text-center
---

# Modelの「今」と<br>Presentationの「今」は違う

<!--
ここで二つ目のキーワードです。

Modelの今と、Presentationの今は同じとは限りません。

Modelではもう3凸かもしれない。
でもPresentationでは、まだ2凸として見せていることが正しい瞬間があります。
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

<!--
ここでは、ModelとPresentationでcommitのタイミングを分けます。

ViewとViewModelのbindingを捨てる必要はありません。
制御したいのは、Modelの結果をいつViewModelへ反映するかです。

UseCaseが完了して、Domain / Model側では結果が確定します。
ただしPresentationでは旧状態のまま演出を再生します。
結果を見せるrevealポイントに来たら、そこで初めてViewModelへ適用します。

するとViewはいつも通りViewModelに従って3凸表示へ変わる。
-->

---
layout: center
class: text-center
---

# ViewModelは<br><span class="text-red-400">ライブミラー</span>ではない

<div class="pt-8 text-xl opacity-80">
今ユーザーに提示している状態を表す
</div>

<!--
ここでさきほどの言葉に戻ります。

ViewModelはModelのライブミラーではありません。
ViewModelは、今ユーザーに何を提示しているかを表します。
-->

---
layout: default
---

# 壁2：画面に映っている。だからView？

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
次の壁は、リアルタイムに動く3Dオブジェクトです。

探索中のプレイヤーは、画面に映っているので一見Viewに見えます。
でも実際には、入力を受けて移動し、そのTransformが敵との距離や会話判定、クエスト到達判定に影響します。

つまりこのGameObjectは、決まった状態を描画しているだけではありません。
自分自身がゲーム世界の次の状態を作っています。
-->

---
layout: center
class: text-center
---

# それ、Viewと呼ぶには<br><span class="text-red-400">仕事をしすぎてない？</span>

<br>

```text
View:        state → appearance

Simulation: state(t) + input → state(t+1)
```

<!--
ここで三つ目のキーワードです。

Viewは、状態から見た目を作るものです。
しかし探索中のプレイヤーは、状態と入力から次の状態を作っています。

それはViewというより、Simulation Actorと考えた方が責務に合います。
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

探索中のプレイヤーでは、Transformの変化そのものがゲーム状態を変えます。
だからSimulation寄りです。

一方、ターン制コマンドバトルなら、Battle Model側で誰が誰に攻撃して何ダメージ、という結果が先に決まっている場合があります。
その後で3Dキャラが走って、剣を振って、ダメージを演出する。

この場合、3Dキャラクターは決定済みのゲーム状態を見せる側なので、かなりView / Presentation Actorとして扱いやすい。
-->

---
layout: center
class: text-center
---

# 3Dかどうかではない

## 状態の<span class="text-red-400">原因</span>か、状態の<span class="text-emerald-400">結果</span>か

<div class="pt-8 text-xl opacity-80">
矢印の向きが違う
</div>

<!--
ここは大事です。

3Dかどうかではありません。
そのオブジェクトがゲーム状態の原因なのか、結果なのか。

探索中のプレイヤーは、Transformが変わることでゲーム状態が変わる。
ターン制バトルの演出では、ゲーム状態が決まった結果としてTransformやAnimatorが動く。

矢印の向きが違います。
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

これらは全部状態ですが、同じ種類の状態ではありません。
寿命も更新頻度も、誰が正とするかも違います。
-->

---
layout: center
class: text-center
---

# ゲームには<br><span class="text-amber-400">「現在」</span>が複数ある

<!--
今回の話をさらに一言でまとめるなら、ゲームには現在が複数ある、です。

Domain上の現在、Simulation上の現在、Presentation上の現在。

この三つが常に一致しているとは限りません。
そして、それぞれが違う意味で正しいことがあります。
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

仕様としては、神殿入口の一定距離内に入ったら進行。
実際に位置を観測するのはTransformやColliderを持つSimulation側です。

そこでTempleEntranceの範囲内にいる、という空間的な意味に変換し、さらにQuest側ではTempleEntranceに到達した、というドメイン上の事実として扱う。

Domainは到達したら進行するというルールを知ることはできます。
でも、ColliderやTransformを自分自身で観測する必要はありません。
-->

---
layout: center
class: text-center
---

# Simulationは世界を観測する

# Domainはそれに意味を与える

<!--
ここも今回のキーワードです。

Simulationは世界を観測する。
Domainはそれに意味を与える。

Transform.positionという実装上の値を、そのままQuest Domainへ持っていく必要はありません。
Quest Domainが欲しいのは、TempleEntranceに到達した、という意味を持った事実です。
-->

---
layout: default
---

# では、MVVMはどこで使うのか

<br>

<div class="p-5 border border-emerald-500/40 rounded-xl bg-emerald-500/10">

## 使いやすいところ

- 設定画面
- ショップ
- インベントリ
- ステータス画面
- HUDの一部
- ターン制バトルのUI / 演出制御

</div>

<br>

<div class="p-5 border border-red-500/40 rounded-xl bg-red-500/10">

## 苦しくなりやすいところ

- 入力で動く3Dプレイヤー
- Physics / Collision がゲーム状態を決める領域
- Transformがクエスト・会話・戦闘判定に関与する領域
- 演出の時間軸を無視したModel即時同期

</div>

<!--
では、MVVMはどこで使うのか。

Presentation StateをViewModelに置けるところでは普通に使えばいいと思います。
設定画面、ショップ、インベントリ、ステータス画面、HUDの一部、ターン制バトルのUIや演出制御。

一方で、入力で動く3Dプレイヤーや、PhysicsやCollisionがゲーム状態を決める領域は、ViewというよりSimulationとして扱った方が自然です。

また、演出の時間軸を無視してModelをViewModelへ即時同期すると、凸演出のような事故が起こります。
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

一方ゲームでは、ModelとPresentationで時間がズレたり、画面に見えているオブジェクト自身がSimulationの状態遷移に参加したりします。

なので、ゲームにMVVMは向かない、と一括りにするより、どこまでがPresentationで、どこからがSimulationなのかを見る方が有用です。
-->

---
layout: center
class: text-center
---

# MVVMが苦しいのではない

## 異なる状態空間を、ひとつに潰すのが苦しい

<!--
かなり短く言うと、MVVMが苦しいのではありません。
異なる状態空間をひとつに潰すのが苦しい。

PresentationにはPresentationの状態があり、SimulationにはSimulationの状態があり、DomainにはDomainの状態があります。

それぞれを分けて考えると、MVVMを使える場所と、別の設計が必要な場所が見えてきます。
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
