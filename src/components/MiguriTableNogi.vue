<script setup>
import { ref } from 'vue'
import html2canvas from 'html2canvas';
let single = 39
let single_end = "th"
let single_title = "Same numbers"
let single_hashtag = "#乃木坂46_samenumbers"
let other_hashtag = ""//"#さつきとーく"
// Noto Color Emoji
let sentence = ""//"🩷「でも皆さんの声が聞こえた瞬間、緊張が一気に自分のパワーになって。」🩵"
let sentence_bold = "「乃木坂46を受けようと思ったきっかけはなんですか？」"
let sentence1 = "最終的に、この道を選んだのは私自身。"
let sentence2 = "他の誰でもなく自分の心に従った結果なのだから、変われる気がするんです。"
let sentence3 = "これからの乃木坂人生、がむしゃらに、全力で駆け抜けるつもりです。"
let sentence_end = ""//"❤️🤍「久しぶりにゆっくり色々話せてよかったし楽しかったー」🩷🩵"
let entry = 0
// max 20 https://senublog.com/nogizaka46-29th-soldout-list/
let center = [] //センター ｾﾝﾀｰ
let w_center = []
let row_1 = [] // フロント ﾌﾛﾝﾄ
let fukujin = []
let senbatsu = []


const response = await fetch(`../nogi/result_${entry}.json`);
const data = await response.json();

let ki3 = ["伊藤理々杏",
  "佐藤楓",
  "中村麗乃",
  "向井葉月",
  "吉田綾乃クリスティー"]

let ki4 = ["金川紗耶",
  "黒見明香",
  "佐藤璃果",
  "柴田柚菜",
  "田村真佑",
  "筒井あやめ",
  "林瑠奈",
  "松尾美佑",
  "矢久保美緒",
  "弓木奈於"]

let ki5 = ["五百城茉央",
  "池田瑛紗",
  "一ノ瀬美空",
  "井上和",
  "岡本姫奈",
  "小川彩",
  "奥田いろは",
  "川﨑桜",
  "菅原咲月",
  "冨里奈央",
  "中西アルノ"]

let ki6 = ["愛宕心響",
  "大越ひなの",
  "小津玲奈",
  "海邉朱莉",
  "川端晃菜",
  "鈴木佑捺",
  "瀬戸口心月",
  "長嶋凛桜",
  "増田三莉音",
  "森平麗心",
  "矢田萌華"]

const getKi = {}

for (let index = 0; index < ki3.length; index++) {
  getKi[ki3[index]] = 3;
}
for (let index = 0; index < ki4.length; index++) {
  getKi[ki4[index]] = 4;
}
for (let index = 0; index < ki5.length; index++) {
  getKi[ki5[index]] = 5;
}
for (let index = 0; index < ki6.length; index++) {
  getKi[ki6[index]] = 6;
}


let parsed = []
let dates = []
let available = [0, 0, 0, 0, 0, 0, 0]  // total, 1ki, 2ki, 3ki, 4ki, 5ki, 6ki
let sold = [0, 0, 0, 0, 0, 0, 0]
let soldThisTime = [0, 0, 0, 0, 0, 0, 0]

for (const memberName in data) {
  if (Object.hasOwnProperty.call(data, memberName)) {
    const memberData = data[memberName];
    const parsedMerberData = { "name": memberName, "available": 0, "sold": 0, "soldThisTime": 0, "list": [] }
    for (const dateData in memberData) {

      if (!dates.includes(dateData)) {
        dates.push(dateData)
      }

      if (Object.hasOwnProperty.call(memberData, dateData)) {

        for (let index = 0; index < memberData[dateData].length; index++) {
          const element = memberData[dateData][index];
          if (element > -1) {
            parsedMerberData.available += 1
            available[0] += 1
            available[getKi[memberName]] += 1


          }
          if (element > 0) {
            parsedMerberData.sold += 1
            sold[0] += 1
            sold[getKi[memberName]] += 1
          }
          if (element == entry) {
            parsedMerberData.soldThisTime += 1
            soldThisTime[0] += 1
            soldThisTime[getKi[memberName]] += 1
          }
          parsedMerberData.list.push(element)
        }


      }
    }
    parsed.push(parsedMerberData)


  }
}

let sorted_parsed = []
// does not work
// for (let index = 0; index < parsed.length; index++) {
//   sorted_parsed.push(parsed[index]);
// }
// does not work as well
// sorted_parsed = Array.from(parsed);
sorted_parsed = JSON.parse(JSON.stringify(parsed))
sorted_parsed.sort((a, b) => {
  if (a.sold == a.available && b.sold != b.available) {
    return -1
  }
  if (a.sold != a.available && b.sold == b.available) {
    return 1
  }

  // both sold, compare who first
  if (a.sold == a.available && b.sold == b.available) {
    if (Math.max(...a.list) < Math.max(...b.list)) {
      return -1
    }
    if (Math.max(...a.list) > Math.max(...b.list)) {
      return 1
    }
    // if same, continue to next comparation
  }

  // compare all previous results from last time
  for (let index = entry; index > 0; index--) {
    let a_sold = a.list.reduce((sold, list_item) => { return list_item > 0 && list_item <= index ? sold += 1 : sold += 0 }, 0)
    let b_sold = b.list.reduce((sold, list_item) => { return list_item > 0 && list_item <= index ? sold += 1 : sold += 0 }, 0)
    console.log(a.list, b.list, a_sold, b_sold, index)
    if (a_sold > b_sold) {
      return -1
    }
    if (a_sold < b_sold) {
      return 1
    }
  }

  // same in every sense 
  return 0
})

for (let index = 0; index < sorted_parsed.length; index++) {
  sorted_parsed[index].list = sorted_parsed[index].list.sort((a, b) => {
    // -1 at end
    if (a == -1) {
      return 1
    }
    if (b == -1) {
      return -1
    }
    // 0 just before -1
    if (a == 0) {
      return 1
    }
    if (b == 0) {
      return -1
    }
    return a - b
  })

}

console.log(parsed, sorted_parsed, dates, available, sold, soldThisTime)

const captureScreenshot = () => {
  const mainElement = document.querySelectorAll(".main")[0];

  const imgElement = document.querySelectorAll("img")[0];

  html2canvas(mainElement).then(canvas => {
    // Convert canvas to data URL
    const dataUrl = canvas.toDataURL('image/png');

    // Open data URL in new tab
    // const newTab = window.open();
    // newTab.document.write('<img src="' + dataUrl + '">');
    imgElement.src = dataUrl
    //mainElement.style.display = "none"
  }).catch(err => {
    console.error('Error capturing screenshot:', err);
  });

}

const one_to_30 = []
for (let index = 1; index <= 30; index++) {
  one_to_30.push(index)
}

setTimeout(captureScreenshot, 1500)
</script>

<template>
  This site should be displayed under 100% zoom<br><br>
  <a :href="`https://fortunemusic.jp/nogizaka_202503/${entry + 1}/goods_list/`">https://fortunemusic.jp/nogizaka_202503/{{
    entry + 1 }}/goods_list/</a><br><br>
  <!-- #姫奈おめでとう<br>
  #やっぱり5期生が大好きなんですよ<br> -->
  乃木坂46 {{ single }}{{ single_end }}シングル「{{ single_title }}」ミーグリ {{ entry }}次抽選結果<br>
  #乃木坂46 #Nogizaka46<br>
  #乃木坂46完売表<br>
  {{ single_hashtag }}<br>
  {{ other_hashtag }}<br>
  <img src="" style="max-width: 720px;"></img>
  <img src="" style="max-width: 720px;"></img>
  <section id="miguri_table" class="main" style="padding: 5px">
    <div class="container svelte-6daqx1">
      <table class="table-bordered svelte-6daqx1" style="border-collapse: collapse;">
        <!-- table-layout: fixed;width: 100%; -->
        <thead>
          <tr>
            <th style="font-size: larger;font-weight: bolder;" class="bottom-border" colspan="38">
              乃木坂46 {{ single }}{{ single_end }}シングル 「{{ single_title }}」
              オンライン ミート＆グリート
              {{ entry }}次抽選結果
            </th>
          </tr>
          <tr>

            <th style="max-width:180px;width:180px;font-weight: normal;" class="right-align">TT@x.com/itsunogi46</th>

            <th v-for="date in dates" :key="date" class="left-border" colspan="5"
              style="width: 100px; font-weight: normal">
              {{ date.replace("（日）", "(日)").replace("（土）", "(土)").replace("（火・祝）", "(火祝)").replace("2024年", "").replace("2025年", "") }}
            </th>
            <th class="left-align left-border" style="max-width: 160px;width:160px;font-weight: normal">
              {{ sold[0] }}/{{ available[0] }} (+{{ soldThisTime[0] }})
            </th>
          </tr>
        </thead>
        <tbody>

          <template v-for="ki in [3, 4, 5, 6]">
            <tr class="top-border bottom-border lighter-purple-bg">

              <td style="font-weight: bold;" class="right-align">
                <span>{{ sold[ki] === available[ki] ? "(完売)" : "" }}</span>
                {{ ki }}期生
              </td>
              <td class="text-white left-border">1</td>
              <td class="text-white">2</td>
              <td class="text-white">3</td>
              <td class="text-white">4</td>
              <td class="text-white">5</td>
              <td class="text-white left-border">1</td>
              <td class="text-white">2</td>
              <td class="text-white">3</td>
              <td class="text-white">4</td>
              <td class="text-white">5</td>
              <td class="text-white left-border">1</td>
              <td class="text-white">2</td>
              <td class="text-white">3</td>
              <td class="text-white">4</td>
              <td class="text-white">5</td>
              <td class="text-white left-border">1</td>
              <td class="text-white">2</td>
              <td class="text-white">3</td>
              <td class="text-white">4</td>
              <td class="text-white">5</td>
              <td class="text-white left-border">1</td>
              <td class="text-white">2</td>
              <td class="text-white">3</td>
              <td class="text-white">4</td>
              <td class="text-white">5</td>
              <td class="text-white left-border">1</td>
              <td class="text-white">2</td>
              <td class="text-white">3</td>
              <td class="text-white">4</td>
              <td class="text-white">5</td>

              <td class="left-align left-border">{{ sold[ki] }}/{{ available[ki] }} (+{{ soldThisTime[[ki]] }})</td>
            </tr>



            <tr v-for="(member, index) in parsed.filter(member => getKi[member.name] == ki)" :key="member" class="">

              <td class="memberName right-align" :class="{ 'lighter-purple-bg': member.sold === member.available }">
                <span :class="{ 'text-bold': member.sold === member.available && Math.max(...member.list) === entry }">
                  {{ member.sold === member.available ? "(" + Math.max(...member.list) + "次完売)" : "" }}
                </span>
                {{ member.name }}

              </td>
              <td v-for="(partStatus, index) in member.list"
                :class="{ 'part-width': true, 'left-border': (index) % 5 === 0, 'sold-this-time': partStatus == entry }">

                {{ partStatus == -1 ? "-" : partStatus == 0 ? " " : partStatus }}
              </td>
              <td class="left-align left-border" :class="{ 'lighter-purple-bg': member.sold === member.available }">
                {{ member.sold }}/{{ member.available }} (+{{ member.soldThisTime }})
                <span>{{ center.includes(member.name) ? "/ ｾﾝﾀｰ" : "" }}</span>
                <span>{{ w_center.includes(member.name) ? "/ Wｾﾝﾀｰ" : "" }}</span>
                <span>{{ row_1.includes(member.name) ? "/ ﾌﾛﾝﾄ" : "" }}</span>
                <span>{{ fukujin.includes(member.name) ? "/ 福神" : "" }}</span>
                <span>{{ senbatsu.includes(member.name) ? "/ 選抜" : "" }}</span>
              </td>
            </tr>
          </template>



        </tbody>

        <tbody>
          <tr>
            <th colspan="38" class="bottom-border top-border">
              <div style="font-size: smaller; font-weight: lighter;"><span style="color: white;">AA</span>{{ sentence }}
              </div>
              <div style="text-align: right;"></div>
              <!--
              <div style="margin: auto; width: max-content;">
                <div style="width: 100%;font-weight: bolder;text-align: left">{{ sentence_bold }}</div>

                <div style="width: 100%;font-weight: normal;text-align: left;">{{ sentence1 }}</div>

                <div style="width: 100%;font-weight: normal;text-align: left;">{{ sentence2 }}</div>

                <div style="width: 100%;font-weight: normal;text-align: left  ;">{{ sentence3 }}</div>
              </div>
              -->

            </th>
          </tr>

        </tbody>
        <!-- x.com/itsunogi46 -->

        <thead>

          <tr>

            <th style="max-width:180px;width:180px;font-weight: normal;" class="right-align bottom-border right-border">
              TT@x.com/itsunogi46</th>

            <th v-for="number in one_to_30" :key="number" colspan="1" style="width: 18.2px; font-weight: normal"
              class="bottom-border">
              {{ number }}
            </th>
            <th class="left-align bottom-border left-border" style=" max-width: 160px;width:160px;font-weight: normal">
              {{ sold[0] }}/{{ available[0] }} (+{{ soldThisTime[0] }})
            </th>
          </tr>
        </thead>
        <tbody>

          <tr v-for="(member, index) in sorted_parsed" :key="member" class="">

            <td class="memberName right-align right-border"
              :class="{ 'lighter-purple-bg': member.sold === member.available }">
              <span :class="{ 'text-bold': member.sold === member.available && Math.max(...member.list) === entry }">
                {{ member.sold === member.available ? "(" + Math.max(...member.list) + "次完売)" : "" }}
              </span>
              {{ member.name }}

            </td>
            <td v-for="(partStatus, index) in member.list" :class="{
              'part-width': true,
              'partStatus1': partStatus == 1,
              'partStatus2': partStatus == 2,
              'partStatus3': partStatus == 3,
              'partStatus4': partStatus == 4,
              'partStatus5': partStatus == 5,
              'partStatus6': partStatus == 6,
              'partStatus7': partStatus == 7,
              'partStatus8': partStatus == 8,
              'partStatus9': partStatus == 9,
              'partStatus10': partStatus == 10,
              'partStatus11': partStatus == 11,
              'partStatus12': partStatus == 12,
              'partStatus13': partStatus == 13,
              'partStatus14': partStatus == 14,
              'partStatus15': partStatus == 15,
              'partStatus16': partStatus == 16,
              'partStatus17': partStatus == 17,
              'partStatus18': partStatus == 18,
              'partStatus19': partStatus == 19,
              'partStatus20': partStatus == 20,
            }">

              {{ partStatus == -1 ? "-" : partStatus == 0 ? " " : partStatus }}
            </td>
            <td class="left-align left-border" :class="{ 'lighter-purple-bg': member.sold === member.available }">
              {{ member.sold }}/{{ member.available }} (+{{ member.soldThisTime }})
              <span>{{ center.includes(member.name) ? "/ ｾﾝﾀｰ" : "" }}</span>
              <span>{{ w_center.includes(member.name) ? "/ Wｾﾝﾀｰ" : "" }}</span>
              <span>{{ row_1.includes(member.name) ? "/ ﾌﾛﾝﾄ" : "" }}</span>
              <span>{{ fukujin.includes(member.name) ? "/ 福神" : "" }}</span>
              <span>{{ senbatsu.includes(member.name) ? "/ 選抜" : "" }}</span>
            </td>
          </tr>






        </tbody>
      </table>
    </div>
    <!--
    <div style="font-size: smaller;"><span style="color: white;">AA</span>{{ sentence_end }}</div>
    -->
  </section>
</template>

<style scoped>
table {
  border: 2px #812990 solid;
  table-layout: fixed;
}

th,
td {
  border: 0.1px #812990 solid;
  height: 5px;
}

.text-bold {
  font-weight: bolder;
}

.lighter-purple-bg {
  background-color: #eac9f0;
}

.partStatus1 {
  background-color: #eac9f0;
  /* 粉紫（固定） */
}

.partStatus2 {
  background-color: #FFCC66;
  /* 浅黄色 */
}

.partStatus3 {
  background-color: #FFE8B3;
  /* 浅黄绿 */
}

.partStatus4 {
  background-color: #E6F5B0;
  /* 柔和草绿色 */
}

.partStatus5 {
  background-color: #CFFFD0;
  /* 浅青绿 */
}

.partStatus6 {
  background-color: #A8F3D5;
  /* 清新薄荷绿 */
}

.partStatus7 {
  background-color: #A8F0E5;
  /* 浅青蓝 */
}

.partStatus8 {
  background-color: #A8E3FF;
  /* 柔和天蓝 */
}

.partStatus9 {
  background-color: #AAD8FF;
  /* 柔和浅蓝 */
}

.partStatus10 {
  background-color: #99CCFF;
  /* 明亮浅蓝 */
}

.partStatus11 {
  background-color: #A5B8FF;
  /* 浅紫蓝 */
}

.partStatus12 {
  background-color: #B3A8FF;
  /* 柔和浅紫 */
}

.partStatus13 {
  background-color: #C5B3FF;
  /* 浅紫偏蓝 */
}

.partStatus14 {
  background-color: #DAC9FF;
  /* 柔和淡紫 */
}

.partStatus15 {
  background-color: #F3D8FF;
  /* 浅粉紫 */
}

.partStatus16 {
  background-color: #FFEAF8;
  /* 柔和粉白 */
}

.partStatus17 {
  background-color: #FFF5EE;
  /* 极浅暖粉白 */
}

.partStatus18 {
  background-color: #FFF8F0;
  /* 柔和暖白 */
}

.partStatus19 {
  background-color: #FFF9F5;
  /* 极淡粉白 */
}

.partStatus20 {
  background-color: #FFFDFE;
  /* 接近纯白（固定） */
}

.light-purple-bg {
  background-color: #daa0e4;
}

.left-border {
  border-left: 2px #812990 solid;

}

.right-border {

  border-right: 2px #812990 solid;
}

.top-border {
  border-top: 2px #812990 solid;

}

.bottom-border {

  border-bottom: 2px #812990 solid;
}

.part-width {
  min-width: 10px;
  width: 10px;
  max-width: 10px;
}

.left-align {
  text-align: left;
  padding-left: 10px;
}

.right-align {
  text-align: right;
  padding-right: 10px;
}

.sold-this-time {
  font-weight: bolder;
  color: #812990;
  background-color: #daa0e4;
}
</style>
