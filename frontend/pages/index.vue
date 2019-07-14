<template>
  <header style="padding: 10px;">
    <h1>SegFault</h1>
    <p>Authentication Test page</p>
    <p>Token: {{ token }}</p>
    <p @click="refreshLoginStatus">Check Status: {{ loggedIn }}</p>
    <p class="line" />
    <div>
      <h2 style="margin-bottom: 10px;">Registration Form</h2>
      <p>username: <input v-model="registration_id" /></p>
      <p>email: <input v-model="registration_email" /></p>
      <p>password: <input v-model="registration_pw1" /></p>
      <p>repeat password: <input v-model="registration_pw2" /></p>
      <button @click="register">Sign up</button>
    </div>
    <div>
      <h2 style="margin-bottom: 10px;">Login Form</h2>
      <p>username: <input v-model="id" /></p>
      <p>password: <input v-model="pw" /></p>
      <button @click="localLogin">Login!</button>
      <button @click="logout">Logout</button><br/>
      <button @click.prevent="socialLogin('naver')">
        Log in with Naver
      </button><br/>
      <button @click.prevent="socialLogin('kakao')">
        Log in with Kakao
      </button><br/>
      <button>
        Forgot password? Reset <strong>here</strong>
      </button><br/>
    </div>
    <div>
      <h2 style="margin-bottom: 10px;">Confirmation Test</h2>
      <div>
        <h3 style="margin-bottom: 7px;">Activate account</h3>
        <p>account activation code: <input v-model="account_activation_code" /></p>
        <button @click="activate_account">Activate</button>
      </div>
      <div>
        <h3 style="margin-bottom: 7px;">Reset account password</h3>
        <p>account email: <input v-model="password_reset_request_email" /></p>
        <button @click="request_password_reset">Reset</button>
      </div>
      <div>
        <h3 style="margin-bottom: 7px;">Confrim password reset</h3>
        <p>password reset code(uid): <input v-model="password_reset_uidb" /></p>
        <p>password reset code(token): <input v-model="password_reset_code" /></p>
        <p>new password: <input v-model="password_reset_pw1" /></p>
        <p>confirm your password: <input v-model="password_reset_pw2" /></p>
        <button @click="reset_password">Confirm</button>
      </div>
      <p>response messages: {{ server_response }}</p>
    </div>
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
      loggedIn: false,
      token: null,
      registration_id: null,
      registration_email: null,
      registration_pw1: null,
      registration_pw2: null,
      id: null,
      pw: null,
      account_activation_code: null,
      password_reset_request_email: null,
      password_reset_uidb: null,
      password_reset_code: null,
      password_reset_pw1: null,
      password_reset_pw2: null,
      server_response: ''
    }
  },
  methods: {
    register() {
      this.$axios.$post('/rest-auth/registration/', {
        username: this.registration_id,
        email: this.registration_email,
        password1: this.registration_pw1,
        password2: this.registration_pw2
      }).then(response => {
        console.log(response)
      })
    },
    localLogin() {
      console.log(this.$data)
      this.$axios.$post('/rest-auth/login/', {
        username: this.id,
        password: this.pw
      })
      .then(res => {
        this.$axios.defaults.headers.common['Authorization'] = `Token ${res.key}`
        console.log(res)
        this.token = res.key
      })
      .catch(err => console.error(err))
    },
    logout() {
      this.$axios.$post('/rest-auth/logout/')
      .then(response => {
        this.server_response = response
        console.log(res)
      })
      .catch(err => console.error(err))
      .finally(() => {
        delete this.$axios.defaults.headers.common['Authorization']
      })
    },
    async refreshLoginStatus() {
      this.loggedIn = await this.$axios.$get('/status/')
    },
    activate_account() {
      this.$axios.$post('/rest-auth/registration/verify-email/', {
        key: this.account_activation_code
      })
      .then(response => {
        this.server_response = response
      })
    },
    request_password_reset() {
      this.$axios.$post('/rest-auth/password/reset/', {
        email: this.password_reset_request_email
      })
      .then(response => {
        this.server_response = response
      })
    },
    reset_password() {
      this.$axios.$post('/rest-auth/password/reset/confirm/', {
        uid: this.password_reset_uidb,
        token: this.password_reset_code,
        new_password1: this.password_reset_pw1,
        new_password2: this.password_reset_pw2
      })
      .then(response => {
        this.server_response = response
      })
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

<style scoped>
  .line {
    margin-top: 10px;
    margin-bottom: 10px;
    border-bottom: 1px solid black;
  }

  p {
    margin-bottom: 4px;
  }

  * div {
    margin: 5px;
    padding: 5px;
    border: 1px solid black;
  }

  * input {
    border-bottom: 1px solid black;
  }

  * button {
    margin: 2px;
    padding: 3px;
    border: 1px solid black;
  }
</style>
