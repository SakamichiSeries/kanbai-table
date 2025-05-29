<script setup>
import { ref } from 'vue'
import html2canvas from 'html2canvas';
let single = 12
let single_end = "th"
let single_title = "Make or Break"
let single_hashtag = "#櫻坂46_MakeorBreak"
let other_hashtag = ""
let sentence = ""//"🩷「11人もいるのに一つの輪でうれしいな~」🩷"  //
let entry = 1
// max 20 https://senublog.com/nogizaka46-29th-soldout-list/
let center = ['的野　美青']
let w_center = []
let row_1 = ['田村　保乃', '山﨑　天']
let row_2 = ['藤吉　夏鈴', '山下　瞳月', '村井　優', '守屋　麗奈', '森田　ひかる']
let row_3 = ['松田　里奈', '谷口　愛季', '中嶋　優月', '向井　純葉', '大園　玲', '村山　美羽']


const response = await fetch(`../saku/result_${entry}.json`);
const data = await response.json();
let ki1 = ['上村　莉菜', '小池　美波', '齋藤　冬優花',]

let ki2 = ['井上　梨名', '遠藤　光莉', '大園　玲', '大沼　晶保', '幸阪　茉里乃', '武元　唯衣', '田村　保乃', '藤吉　夏鈴', '増本　綺良', '松田　里奈', '森田　ひかる', '守屋　麗奈', '山﨑　天']

let ki3 = ['石森　璃花', '遠藤　理子', "小田倉　麗奈", '小島　凪紗', '谷口　愛季', '中嶋　優月', '的野　美青', '向井　純葉', '村井　優', '村山　美羽', '山下　瞳月']

let ki4 = []

const getKi = {}

for (let index = 0; index < ki1.length; index++) {
  getKi[ki1[index]] = 1;
}
for (let index = 0; index < ki2.length; index++) {
  getKi[ki2[index]] = 2;
}
for (let index = 0; index < ki3.length; index++) {
  getKi[ki3[index]] = 3;
}
for (let index = 0; index < ki4.length; index++) {
  getKi[ki4[index]] = 4;
}




let parsed = []
let dates = []
let available = [0, 0, 0, 0, 0, 0]  // total, 1ki, 2ki, 3ki, 4ki, 5ki
let sold = [0, 0, 0, 0, 0, 0]
let soldThisTime = [0, 0, 0, 0, 0, 0]

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

let dates1 = [dates[0], dates[1], dates[2], dates[3], dates[4], dates[5]]
let dates2 = [dates[0], dates[1], dates[2], dates[6], dates[7], dates[8]]

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

const one_to_36 = []
for (let index = 1; index <= 36; index++) {
  one_to_36.push(index)
}

setTimeout(captureScreenshot, 1500)
</script>

<template>
  This site should be displayed under 100% zoom<br><br>
  <a :href="`https://fortunemusic.jp/sakurazaka_202410/${entry + 1}/goods_list/`">https://fortunemusic.jp/sakurazaka_202410/{{
    entry + 1 }}/goods_list/</a><br><br>
  <!-- #姫奈おめでとう<br>
  #やっぱり5期生が大好きなんですよ<br> -->
  櫻坂46 {{ single }}{{ single_end }}シングル「{{ single_title }}」ミーグリ {{ entry }}次抽選結果<br>
  #櫻坂46 #Sakurazaka46<br>
  #櫻坂46完売表<br>
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
              櫻坂46 {{ single }}{{ single_end }}シングル 「{{
                single_title }}」
              オンライン ミート＆グリート
              {{ entry }}次抽選結果
            </th>
          </tr>
          <tr>

            <th style="max-width:180px;width:180px;font-weight: normal;" class="right-align">TT@x.com/itsunogi46</th>

            <th v-for="date in dates" :key="date" class="left-border" colspan="6"
              style="width: 120px; font-weight: normal">
              {{ date.replace("（日）", "(日)").replace("（日・祝）", "(日・祝)").replace("（土）", "(土)").replace("2024年",
                "").replace("2025年", "") }}
            </th>
            <th class="left-align left-border" style="max-width: 170px;width:170px;font-weight: normal">
              {{ sold[0] }}/{{ available[0] }} (+{{ soldThisTime[0] }})
            </th>
          </tr>
        </thead>
        <tbody>

          <template v-for="ki in [2, 3]">
            <tr class="top-border bottom-border lighter-pink-bg">

              <td style="font-weight: bold;" class="right-align">
                <span>{{ sold[ki] === available[ki] ? "(完売)" : "" }}</span>
                {{ ki }}期生
              </td>
              <td class="text-white left-border">1</td>
              <td class="text-white">2</td>
              <td class="text-white">3</td>
              <td class="text-white">4</td>
              <td class="text-white">5</td>
              <td class="text-white">6</td>
              <td class="text-white left-border">1</td>
              <td class="text-white">2</td>
              <td class="text-white">3</td>
              <td class="text-white">4</td>
              <td class="text-white">5</td>
              <td class="text-white">6</td>
              <td class="text-white left-border">1</td>
              <td class="text-white">2</td>
              <td class="text-white">3</td>
              <td class="text-white">4</td>
              <td class="text-white">5</td>
              <td class="text-white">6</td>
              <td class="text-white left-border">1</td>
              <td class="text-white">2</td>
              <td class="text-white">3</td>
              <td class="text-white">4</td>
              <td class="text-white">5</td>
              <td class="text-white">6</td>
              <td class="text-white left-border">1</td>
              <td class="text-white">2</td>
              <td class="text-white">3</td>
              <td class="text-white">4</td>
              <td class="text-white">5</td>
              <td class="text-white">6</td>
              <td class="text-white left-border">1</td>
              <td class="text-white">2</td>
              <td class="text-white">3</td>
              <td class="text-white">4</td>
              <td class="text-white">5</td>
              <td class="text-white">6</td>

              <td class="left-align left-border">{{ sold[ki] }}/{{ available[ki] }} (+{{ soldThisTime[[ki]] }})</td>
            </tr>



            <tr v-for="(member, index) in parsed.filter(member => getKi[member.name] == ki)" :key="member" class="">

              <td class="memberName right-align" :class="{ 'lighter-pink-bg': member.sold === member.available }">
                <span :class="{ 'text-bold': member.sold === member.available && Math.max(...member.list) === entry }">
                  {{ member.sold === member.available ? "(" + Math.max(...member.list) + "次完売)" : "" }}
                </span>
                {{ member.name.replace("　", "") }}

              </td>
              <td v-for="(partStatus, index) in member.list"
                :class="{ 'part-width': true, 'left-border': (index) % 6 === 0, 'sold-this-time': partStatus == entry }">

                {{ partStatus == -1 ? "-" : partStatus == 0 ? " " : partStatus }}
              </td>
              <td class="left-align left-border" :class="{ 'lighter-pink-bg': member.sold === member.available }">
                {{ member.sold }}/{{ member.available }} (+{{ member.soldThisTime }})
                <span>{{ center.includes(member.name) ? "/ ｾﾝﾀｰ" : "" }}</span>
                <span>{{ w_center.includes(member.name) ? "/ Wｾﾝﾀｰ" : "" }}</span>
                <span>{{ row_1.includes(member.name) ? "/ ﾌﾛﾝﾄ" : "" }}</span>
                <span>{{ row_2.includes(member.name) ? "/ 2列目" : "" }}</span>
                <span>{{ row_3.includes(member.name) ? "/ 3列目" : "" }}</span>
              </td>
            </tr>
          </template>



        </tbody>


        <tbody>
          <tr>
            <th colspan="38" class="bottom-border top-border">
              <div style="font-size: smaller;"><span style="color: white;">AA</span>{{ sentence }}
              </div>
              <div style="text-align: right;"></div>

            </th>
          </tr>

        </tbody>
        <!-- x.com/itsunogi46 -->

        <thead>
          <tr>
            <th style="font-size: larger;font-weight: bolder;" class="bottom-border" colspan="38">
              櫻坂46 {{ single }}{{ single_end }}シングル 「{{
                single_title }}」
              オンライン ミート＆グリート
              {{ entry }}次抽選結果
            </th>
          </tr>
          <tr>

            <th style="max-width:180px;width:180px;font-weight: normal;" class="right-align bottom-border right-border">
              TT@x.com/itsunogi46</th>

            <th v-for="number in one_to_36" :key="number" colspan="1" style="width: 18px; font-weight: normal"
              class="bottom-border">
              {{ number }}
            </th>
            <th class="left-align bottom-border left-border" style="max-width: 170px;width:170px;font-weight: normal">
              {{ sold[0] }}/{{ available[0] }} (+{{ soldThisTime[0] }})
            </th>
          </tr>
        </thead>
        <tbody>

          <tr v-for="(member, index) in sorted_parsed" :key="member" class="">

            <td class="memberName right-align right-border"
              :class="{ 'lighter-pink-bg': member.sold === member.available }">
              <span :class="{ 'text-bold': member.sold === member.available && Math.max(...member.list) === entry }">
                {{ member.sold === member.available ? "(" + Math.max(...member.list) + "次完売)" : "" }}
              </span>
              {{ member.name.replace("　", "") }}

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
            <td class="left-align left-border" :class="{ 'lighter-pink-bg': member.sold === member.available }">
              {{ member.sold }}/{{ member.available }} (+{{ member.soldThisTime }})
              <span>{{ center.includes(member.name) ? "/ ｾﾝﾀｰ" : "" }}</span>
              <span>{{ w_center.includes(member.name) ? "/ Wｾﾝﾀｰ" : "" }}</span>
              <span>{{ row_1.includes(member.name) ? "/ ﾌﾛﾝﾄ" : "" }}</span>
              <span>{{ row_2.includes(member.name) ? "/ 2列目" : "" }}</span>
              <span>{{ row_3.includes(member.name) ? "/ 3列目" : "" }}</span>
            </td>
          </tr>




        </tbody>
      </table>
    </div>
  </section>
</template>

<style scoped>
/* 表格样式 */
table {
  border: 2px #E68AAE solid;
  /* 浅粉色边框 */
  table-layout: fixed;
}

th,
td {
  border: 0.1px #E68AAE solid;
  height: 5px;
}

.text-bold {
  font-weight: bolder;
}

.lighter-pink-bg {
  background-color: #FDE9F2;
  /* 淡粉背景色 */
}

/* 不同状态的背景色调整为浅粉色系 */
.partStatus1 {
  background-color: #FDE9F2;
}

.partStatus2 {
  background-color: #FBDDEB;
  /* 浅粉 */
}

.partStatus3 {
  background-color: #F9D1E4;
  /* 浅粉偏紫 */
}

.partStatus4 {
  background-color: #F7C5DD;
  /* 柔和粉紫 */
}

.partStatus5 {
  background-color: #F5B9D6;
  /* 明亮粉紫 */
}

.partStatus6 {
  background-color: #F3ADCF;
  /* 清新粉 */
}

.partStatus7 {
  background-color: #F1A1C8;
  /* 青粉 */
}

.partStatus8 {
  background-color: #EF95C1;
  /* 深粉 */
}

.partStatus9 {
  background-color: #ED89BA;
  /* 柔和粉红 */
}

.partStatus10 {
  background-color: #EB7DB3;
  /* 明亮粉红 */
}

.partStatus11 {
  background-color: #E971AC;
  /* 浅紫粉 */
}

.partStatus12 {
  background-color: #E765A5;
  /* 浅紫偏粉 */
}

.partStatus13 {
  background-color: #E5599E;
  /* 深粉 */
}

.partStatus14 {
  background-color: #E34D97;
  /* 柔和深粉 */
}

.partStatus15 {
  background-color: #E14190;
  /* 深紫粉 */
}

.partStatus16 {
  background-color: #DF3589;
  /* 深粉偏紫 */
}

.partStatus17 {
  background-color: #DD2982;
  /* 极深粉 */
}

.partStatus18 {
  background-color: #DB1D7B;
  /* 柔和暗粉 */
}

.partStatus19 {
  background-color: #D91174;
  /* 深粉红 */
}

.partStatus20 {
  background-color: #D7056D;
  /* 几乎纯红粉 */
}

.light-pink-bg {
  background-color: #F7C5DD;
  /* 浅粉背景色 */
}

/* 边框样式 */
.left-border {
  border-left: 2px #E68AAE solid;
}

.right-border {
  border-right: 2px #E68AAE solid;
}

.top-border {
  border-top: 2px #E68AAE solid;
}

.bottom-border {
  border-bottom: 2px #E68AAE solid;
}

.part-width {
  max-width: 10px;
}

/* 对齐和文本样式 */
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
  color: #E68AAE;
  background-color: #F7C5DD;
}
</style>
