<template>
  <header>
    <h1>SegFault</h1>
    <p>Test page</p>
    <nuxt-link to="/avatars">
      Go get some data
    </nuxt-link>
    <br/>
    <button @click.prevent="socialLogin('naver')">
      Log in with Naver
    </button>
    <br/>
    <button @click.prevent="socialLogin('kakao')">
      Log in with Kakao
    </button>
    <h3 @click="refreshLoginStatus">Login Status: {{ loggedIn }}</h3>
  </header>
</template>

<script>
export default {
  head() {
    return {
      title: "SegFault"
    }
  },
  data() {
    return {
      loggedIn: false
    }
  },
  methods: {
    async refreshLoginStatus() {
      this.loggedIn = await this.$axios.$get('/status/')
    },
    socialLogin(provider) {
      let host = 'http://localhost:8000/'
      let href
      switch(provider) {
        case 'naver':
          href = 'accounts/naver/login'
          break
        case 'kakao':
          href = 'accounts/kakao/login'
          break
        default:
          console.error(`Provider ${provider} is not supported.`)
          return null
      }
      return this._popup(host + href)
    },
    _popup(href) {
      let child    = window.open(href, '', '', false)
      let timeout  = 10000 // in milliseconds
      let interval = 100   // in milliseconds, checking frequency
      let timer    = setInterval(() => {
        timeout -= interval
        if (child.closed) {
          clearInterval(timer)
          console.log('Login process is done')
        }
        else if (timeout < 0) {
          clearInterval(timer)
        }
      }, interval)
    }
  }
}
</script>
