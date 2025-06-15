<script setup>
import { ref } from 'vue'
import html2canvas from 'html2canvas';

let title = "14thシングル『Love yourself!』 "
let single_hashtag = "#日向坂46_Loveyourself"

let sentence = ""
let entry = 2.5 // entry can be "1", "1.5", "2", "2.5", "3" ...
let result_name = "2次応募保障結果"//"1次応募保障結果"
let center = ['小坂菜緒']
let w_center = []
let row_1 = ["金村美玖", "上村ひなの", "正源司陽子", '藤嶌果歩']
let row_2 = ["山下葉留花", "森本茉莉", "松田好花", "河田陽菜", "富田鈴花", "平尾帆夏", "宮地すみれ"]
let row_3 = ["石塚瑶季", "小西夏菜実", "清水理央", "竹内希来里", "平岡海月", "渡辺莉奈", "髙橋未来虹", "山口陽世",]


const response = await fetch(`../hina_special/result_${entry}.json`);
const data = await response.json();

let ki1 = ["加藤史帆", "佐々木久美", "佐々木美玲", "高瀬愛奈", "東村芽依",]

let ki2 = ["金村美玖", "河田陽菜", "小坂菜緒", "富田鈴花", "丹生明里", "濱岸ひより", "松田好花",]

let ki3 = ["上村ひなの", "髙橋未来虹", "森本茉莉", "山口陽世",]

let ki4 = ["石塚瑶季", "小西夏菜実", "清水理央", "正源司陽子", "竹内希来里", "平尾帆夏", "平岡海月", "藤嶌果歩", "宮地すみれ", "山下葉留花", "渡辺莉奈",]

let ki5 = ["大田美月", "大野愛実", "片山紗希", "蔵盛妃那乃", "坂井新奈", "佐藤優羽", "下田衣珠季", "高井俐香", "鶴崎仁香", "松尾桜",]

const getKi = {}

for (let index = 0; index < ki2.length; index++) {
  getKi[ki2[index]] = 2;
}
for (let index = 0; index < ki3.length; index++) {
  getKi[ki3[index]] = 3;
}
for (let index = 0; index < ki4.length; index++) {
  getKi[ki4[index]] = 4;
}
for (let index = 0; index < ki5.length; index++) {
  getKi[ki5[index]] = 5;
}



let parsed = []
let dates = []
let available = [0, 0, 0, 0, 0, 0, 0]  // total, 1ki, 2ki, 3ki, 4ki, 5ki
let sold = [0, 0, 0, 0, 0, 0, 0]
let soldThisTime = [0, 0, 0, 0, 0, 0, 0]

for (const memberName in data) {
  if (Object.hasOwnProperty.call(data, memberName)) {
    const memberData = data[memberName];
    const parsedMerberData = { "name": memberName, "available": 0, "sold": 0, "soldThisTime": 0, "list": [], "P": "" }
    for (const dateData in memberData) {

      if (!dates.includes(dateData) && dateData != "P") {

        dates.push(dateData)
      }
      //dates = ["1月26日", "2月2日", "2月16日"]

      if (Object.hasOwnProperty.call(memberData, dateData)) {


        for (let index = 0; index < memberData[dateData].length; index++) {
          if (dateData == "P") {
            parsedMerberData.P = memberData[dateData]
            break
          }

          const element = memberData[dateData][index];
          // entry can be -1, 0, 1, 1.5, 2, 2.5, 3, 3.5 ...
          if (element != -1) {
            parsedMerberData.available += 1
            available[0] += 1
            available[getKi[memberName]] += 1
          }
          if (element > 0) {
            parsedMerberData.sold += 1
            sold[0] += 1
            sold[getKi[memberName]] += 1
          }
          if (element == entry) { // entry can be -1, 0, 1, 1.5, 2, 2.5, 3, 3.5 ...
            parsedMerberData.soldThisTime += 1
            soldThisTime[0] += 1
            soldThisTime[getKi[memberName]] += 1
          }
          if (element == 0) {
            parsedMerberData.list.push(0)
          }
          else {
            parsedMerberData.list.push(element)
          }

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
  for (let index = entry; index > 0; index -= 0.5) {
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
    //     console.log(dataUrl)
    //     setTimeout(() => {
    //     window.open(dataUrl, "_blank");
    // }, 100);
    // const link = document.createElement('a');
    // link.href = dataUrl;
    // link.target = '_blank';
    // link.click();
    // const newWindow = window.open();
    // if (newWindow) {
    //     newWindow.document.write(`<img src="${dataUrl}" alt="Canvas Image"/>`);
    // } else {
    //     console.error("Popup blocked or window.open failed!");
    // }
    // Open data URL in new tab
    // const newTab = window.open();
    // newTab.document.write('<img src="' + dataUrl + '">');
    imgElement.src = dataUrl
    // //mainElement.style.display = "none"
  }).catch(err => {
    console.error('Error capturing screenshot:', err);
  });

}

const one_to_12 = []
for (let index = 1; index <= 12; index++) {
  one_to_12.push(index)
}

setTimeout(captureScreenshot, 1500)
setTimeout(() => { window.location.reload() }, 30000)
</script>

<template>
  This site should be displayed under 100% zoom<br><br>
  <a :href="`https://ticket.fortunemeets.app/data/nogizaka46/38th/config.json`">
    https://ticket.fortunemeets.app/data/nogizaka46/38th/config.json
  </a>
  <br><br>
  <a :href="`https://ticket.fortunemeets.app/nogizaka46/38th`">
    https://ticket.fortunemeets.app/nogizaka46/38th
  </a>
  <br><br>
  <!-- #姫奈おめでとう<br>
  #やっぱり5期生が大好きなんですよ<br> -->
  日向坂46 {{ title }} スペシャル抽選応募 {{ result_name }}<br>
  #日向坂46 #Hinatazaka46<br>
  #日向坂46完売表<br>
  {{ single_hashtag }}<br>
  {{ other_hashtag }}<br>
  <img src="" style="max-width: 800px;"></img>
  <img src="" style="max-width: 800px;"></img>
  <section id="miguri_table" class="main" style="padding: 5px">
    <div class="container svelte-6daqx1">
      <table class="table-bordered svelte-6daqx1" style="border-collapse: collapse;">
        <!-- table-layout: fixed;width: 100%; -->

        <thead>
          <tr>
            <th style="font-size: larger;font-weight: bolder;" class="bottom-border" colspan="15">
              日向坂46 {{ title }}
              スペシャル抽選応募 {{ result_name }}</th>
          </tr>
          <tr>

            <th style="max-width:200px;width:200px;font-weight: normal;" class="right-align">TT@x.com/itsunogi46</th>

            <th class="left-border" colspan="4" style="width: 150px; font-weight: normal">
              {{ dates[0].toString().replace("（日）", "(日)").replace("2024年", "").replace("2025年", "") }}(東京)
            </th>

            <th class="left-border" colspan="4" style="width: 150px; font-weight: normal">
              {{ dates[1].toString().replace("（日）", "(日)").replace("2024年", "").replace("2025年", "") }}(京都)
            </th>

            <th class="left-border" colspan="4" style="width: 150px; font-weight: normal">
              {{ dates[2].toString().replace("（日）", "(日)").replace("2024年", "").replace("2025年", "") }}(オンライン)
            </th>



            <th class="left-border left-align" style="max-width: 160px;width:160px;font-weight: normal">
              {{ sold[0] }}/{{ available[0] }} (+{{ soldThisTime[0] }})
            </th>
          </tr>
        </thead>
        <tbody>

          <template v-for="ki in [2, 3, 4, 5]">
            <tr class="top-border bottom-border lighter-blue-bg">

              <td style="font-weight: bold;" class="right-align">
                <span>{{ sold[ki] === available[ki] ? "(完売)" : "" }}</span>
                {{ ki }}期生
              </td>
              <td class="text-white left-border">1</td>
              <td class="text-white">2</td>
              <td class="text-white">3</td>
              <td class="text-white">4</td>

              <td class="text-white left-border">1</td>
              <td class="text-white">2</td>
              <td class="text-white">3</td>
              <td class="text-white">4</td>

              <td class="text-white left-border">1</td>
              <td class="text-white">2</td>
              <td class="text-white">3</td>
              <td class="text-white">4</td>

              <td class="left-align left-border">{{ sold[ki] }}/{{ available[ki] }} (+{{ soldThisTime[[ki]] }})</td>
            </tr>



            <tr v-for="(member, index) in parsed.filter(member => getKi[member.name] == ki)" :key="member" class="">

              <td class="memberName right-align" :class="{ 'lighter-blue-bg': member.sold === member.available }">
                <span :class="{ 'text-bold': member.sold === member.available && Math.max(...member.list) === entry }">
                  {{ member.sold === member.available ? "(" + (Math.max(...member.list) +
                    "次").toString().replace(".5次", "次保障") + "完売)" : "" }}
                </span>
                {{ member.name }}

              </td>
              <td v-for="(partStatus, index) in member.list"
                :class="{ 'part-width': true, 'left-border': (index) % 4 === 0, 'sold-this-time': partStatus == entry }">
                {{ partStatus == -1 ? "-" : partStatus == 0 ? " " : partStatus.toString().replace(".5", "保") }}
              </td>



              <td class="left-align left-border" :class="{ 'lighter-blue-bg': member.sold === member.available }">
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




        <thead>
          <tr>
            <th style="font-size: larger;font-weight: bolder;" class="bottom-border top-border" colspan="15">
              日向坂46 {{ title }}
              スペシャル抽選応募 {{ result_name }}</th>
          </tr>
          <tr>

            <th style="max-width:200px;width:200px;font-weight: normal;" class="right-align bottom-border right-border">
              TT@x.com/itsunogi46</th>

            <th v-for="number in one_to_12" :key="number" colspan="1" style="width: 18px; font-weight: normal"
              class="bottom-border">
              {{ number }}
            </th>
            <th class="left-align bottom-border left-border" style="max-width: 140px;width:140px;font-weight: normal">
              {{ sold[0] }}/{{ available[0] }} (+{{ soldThisTime[0] }})
            </th>
          </tr>
        </thead>
        <tbody>

          <tr v-for="(member, index) in sorted_parsed" :key="member" class="">

            <td class="memberName right-align right-border"
              :class="{ 'lighter-blue-bg': member.sold === member.available }">
              <span :class="{ 'text-bold': member.sold === member.available && Math.max(...member.list) === entry }">
                {{ member.sold === member.available ? "(" + (Math.max(...member.list) +
                  "次").toString().replace(".5次", "次保障") + "完売)" : "" }}
              </span>
              {{ member.name }}

            </td>
            <td v-for="(partStatus, index) in member.list" :class="{
              'part-width': true,
              'partStatus1': partStatus == 1,
              'partStatus2': partStatus == 1.5,
              'partStatus3': partStatus == 2,
              'partStatus4': partStatus == 2.5,
              'partStatus5': partStatus == 3,
              'partStatus6': partStatus == 3.5,
              'partStatus7': partStatus == 4,
              'partStatus8': partStatus == 4.5,
              // 'partStatus9': partStatus == 9,
              // 'partStatus10': partStatus == 10,
              // 'partStatus11': partStatus == 11,
              // 'partStatus12': partStatus == 12,
              // 'partStatus13': partStatus == 13,
              // 'partStatus14': partStatus == 14,
              // 'partStatus15': partStatus == 15,
              // 'partStatus16': partStatus == 16,
              // 'partStatus17': partStatus == 17,
              // 'partStatus18': partStatus == 18,
              // 'partStatus19': partStatus == 19,
              // 'partStatus20': partStatus == 20,
            }">

              {{ partStatus == -1 ? "-" : partStatus == 0 ? " " : partStatus.toString().replace(".5", "保") }}
            </td>
            <td class="left-align left-border" :class="{ 'lighter-blue-bg': member.sold === member.available }">
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
  border: 2px #4A90E2 solid;
  /* 浅蓝色边框 */
  table-layout: fixed;
}

th,
td {
  border: 0.1px #4A90E2 solid;
  height: 5px;
}

.text-bold {
  font-weight: bolder;
}

.lighter-blue-bg {
  background-color: #EAF4FE;
  /* 淡蓝背景色 */
}

/* 不同状态的背景色调整为淡蓝色系 */
.partStatus1 {
  background-color: #E9F5FD;
  /* 淡天蓝 */
}

.partStatus2 {
  background-color: #DDEFFD;
  /* 浅蓝 */
}

.partStatus3 {
  background-color: #D1E9FC;
  /* 柔和浅蓝 */
}

.partStatus4 {
  background-color: #C5E3FC;
  /* 柔和天蓝 */
}

.partStatus5 {
  background-color: #B9DDFB;
  /* 明亮天蓝 */
}

.partStatus6 {
  background-color: #ADD7FB;
  /* 清新蓝 */
}

.partStatus7 {
  background-color: #A1D1FA;
  /* 纯净蓝 */
}

.partStatus8 {
  background-color: #95CBFA;
  /* 柔和蓝 */
}

.partStatus9 {
  background-color: #89C5F9;
  /* 轻盈蓝 */
}

.partStatus10 {
  background-color: #7DBFF9;
  /* 亮蓝 */
}

.partStatus11 {
  background-color: #71B9F8;
  /* 浅湖蓝 */
}

.partStatus12 {
  background-color: #65B3F8;
  /* 深湖蓝 */
}

.partStatus13 {
  background-color: #59ADF7;
  /* 柔和深蓝 */
}

.partStatus14 {
  background-color: #4DA7F7;
  /* 明亮深蓝 */
}

.partStatus15 {
  background-color: #41A1F6;
  /* 深蓝 */
}

.partStatus16 {
  background-color: #359BF6;
  /* 经典蓝 */
}

.partStatus17 {
  background-color: #2995F5;
  /* 深浅蓝 */
}

.partStatus18 {
  background-color: #1D8FF5;
  /* 暗蓝 */
}

.partStatus19 {
  background-color: #1189F4;
  /* 深邃蓝 */
}

.partStatus20 {
  background-color: #0573D7;
  /* 近于纯蓝 */
}

.light-blue-bg {
  background-color: #B3DFFD;
  /* 浅蓝背景色 */
}

/* 边框样式 */
.left-border {
  border-left: 2px #4A90E2 solid;
}

.right-border {
  border-right: 2px #4A90E2 solid;
}

.top-border {
  border-top: 2px #4A90E2 solid;
}

.bottom-border {
  border-bottom: 2px #4A90E2 solid;
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
  color: #4A90E2;
  background-color: #B3DFFD;
}
</style>
