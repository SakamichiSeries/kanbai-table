<script setup>
import { ref, watch, onMounted } from 'vue';
import MiguriTableNogi_Special from './components/MiguriTableNogi_Special.vue'
import MiguriTableSaku_Special from './components/MiguriTableSaku_Special.vue'
import MiguriTableHina_Special from './components/MiguriTableHina_Special.vue'

import MiguriTableNogi_Tieba from './components/MiguriTableNogi_Tieba.vue';

import MiguriTableNogi from './components/MiguriTableNogi.vue';
import MiguriTableSaku from './components/MiguriTableSaku.vue';
import MiguriTableHina from './components/MiguriTableHina.vue';

import MiguriTableSaku_Album from './components/MiguriTableSaku_Album.vue';

// 保存当前需要渲染的组件
const currentComponent = ref('MiguriTableNogi');

// 组件映射表
const componentsMap = {
  n: MiguriTableNogi,
  ns: MiguriTableNogi_Special,
  nt: MiguriTableNogi_Tieba,
  s: MiguriTableSaku,
  ss: MiguriTableSaku_Special,
  sa: MiguriTableSaku_Album,
  h: MiguriTableHina,
  hs: MiguriTableHina_Special,
};
const current_url = window.location.href.split('#')[0];
let html = ""
for (const element in componentsMap) {
  html += "<a href='" + current_url + "#" + element + "'>" + current_url + "#" + element + "</a><br>"
}
console.log(html)

// 更新组件方法
const updateComponent = () => {
  const hash = window.location.hash.slice(1); // 获取#后面的值
  currentComponent.value = componentsMap[hash]; // 默认是nogi
};

// 初始化和监听hash变化
onMounted(() => {
  updateComponent();
  window.addEventListener('hashchange', updateComponent); // 监听哈希变化
});

</script>

<template>
  <Suspense>
    <div>
      <div v-html="html"></div>
      <component :is="currentComponent" />
    </div>
  </Suspense>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}

.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}

.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
