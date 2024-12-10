<script setup>import { ref, onMounted } from 'vue';
import axios from 'axios';
import {message} from "ant-design-vue";

const captchaImage = ref('');
const userInputCaptcha = ref('');

const fetchCaptcha = async () => {
  try {
    const response = await axios.get('/api/captcha', { responseType: 'blob' });
    const url = window.URL.createObjectURL(new Blob([response.data]));
    captchaImage.value = url;
  } catch (error) {
    console.error('Error fetching captcha:', error);
  }
};

const submitCaptcha = async () => {
  console.log(userInputCaptcha.value);
  if (!userInputCaptcha.value) {
    console.error('验证码为空');
    return;
  }
  try {
    const response = await axios.post('/api/verify-captcha', {
      code: userInputCaptcha.value
    }, {
          headers: {'Content-Type':'application/x-www-form-urlencoded'},
          emulateJSON: true
    });
    const result = response.data;
    console.log(result);
    if (result.result) {
      message.success('验证成功');
    } else {
      message.error('验证失败');
    }
  } catch (error) {
    console.error('请求失败:', error);
  }
};

onMounted(() => {
  fetchCaptcha();
});
</script>

<template>
  <h2>这是验证码页面</h2>
  <img :src="captchaImage" alt="验证码" @click="fetchCaptcha" />
  <input type="text" v-model="userInputCaptcha" placeholder="请输入验证码" />
  <button @click="submitCaptcha">提交</button>
</template>

<style scoped>
img {
  width: 200px;
  height: auto;
  cursor: pointer;
}

input {
  margin-top: 10px;
  padding: 5px;
  width: 200px;
}

button {
  margin-top: 10px;
  padding: 5px 10px;
}
</style>
