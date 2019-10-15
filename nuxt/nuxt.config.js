import colors from 'vuetify/es5/util/colors'

export default {
  mode: 'spa',
  /*
  ** Headers of the page
  */
  head: {
    titleTemplate: '%s - ' + process.env.npm_package_name,
    title: process.env.npm_package_name || '',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: process.env.npm_package_description || '' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
,
      {
        rel: 'stylesheet',
        href:
          'https://fonts.googleapis.com/css?family=Roboto:300,400,500,700|Material+Icons'
      }
    ]
  },
  /*
  ** Customize the progress-bar color
  */
  loading: { color: '#fff' },
  /*
  ** Global CSS
  */
  css: [

  ],
  /*
  ** Plugins to load before mounting the App
  */
  plugins: [
    { src: '~/plugins/axios.js', ssr: false },
    { src: '~/plugins/vee-validate.js', ssr: false },
    { src: '~/plugins/firebase.js', ssr: false }
  ],
  /*
  ** Nuxt.js modules
  */
  modules: [
    '@nuxtjs/vuetify',
    // Doc: https://axios.nuxtjs.org/usage
    '@nuxtjs/axios',
    '@nuxtjs/proxy',
    '@nuxtjs/pwa'
  ],
  /*
  ** Axios module configuration
  ** See https://axios.nuxtjs.org/options
  */
  axios: {
    baseURL: 'http://localhost:8000/'
  },
  /*
  ** Proxy
  */
  proxy: {
    '/static': {
      target: 'http://localhost:8000',
    },
  },
  /*
  ** vuetify module configuration
  ** https://github.com/nuxt-community/vuetify-module
  */
  vuetify: {
    theme: {
      primary: colors.blue.darken2,
      accent: colors.grey.darken3,
      secondary: colors.amber.darken3,
      info: colors.teal.lighten1,
      warning: colors.amber.base,
      error: colors.deepOrange.accent4,
      success: colors.green.accent3,
    }
  },
  /*
   ** PWA Setting - Rena Makise
   */
  pwa: {
    manifest: {
      name: 'SegFault',
      short_name: 'SegFault',
      description: 'Dev Community',
      lang: 'ko-KR',
      start_url: '/',
      display: 'standalone',
      theme_color: '#263238',
      background_color: '#263238',
      gcm_sender_id: '103953800507',
      icons: [{
        "src": "/static/icons/android-icon-36x36.png",
        "sizes": "36x36",
        "type": "image/png",
        "density": "0.75"
      }, {
       "src": "/static/icons/android-icon-48x48.png",
       "sizes": "48x48",
       "type": "image/png",
       "density": "1.0"
      }, {
        "src": "/static/icons/android-icon-72x72.png",
        "sizes": "72x72",
        "type": "image/png",
        "density": "1.5"
       }, {
        "src": "/static/icons/android-icon-96x96.png",
        "sizes": "96x96",
        "type": "image/png",
        "density": "2.0"
       }, {
        "src": "/static/icons/android-icon-144x144.png",
        "sizes": "144x144",
        "type": "image/png",
        "density": "3.0"
       }, {
        "src": "/static/icons/android-icon-192x192.png",
        "sizes": "192x192",
        "type": "image/png",
        "density": "4.0"
      }, {
        "src": "/static/icons/icon.png",
        "sizes": "512x512",
        "type": "image/png"
      }]
    },
    workbox: {
      dev: true,
      runtimeCaching: [
        {
          urlPattern: "/*",
          handler: "networkFirst",
          method: "GET"
        }
      ],
      offlinePage: "offline.html"
    }
  },
  /*
  ** Build configuration
  */
  build: {
    /*
    ** You can extend webpack config here
    */
    extend(config, ctx) {
    }
  },
  /*
  ** Rewrite 
  */
  router: {
    base: process.env.NODE_ENV === 'production' ? '/static' : '/'
  }
}

module.exports = {
  head: {
    link: [
      { rel: 'shortcut icon', href: '/static/icons/favicon.ico' }, 
      { rel: 'apple-touch-icon', sizes: '57x57', href: '/static/icons/apple-icon-57x57.png' },
      { rel: 'apple-touch-icon', sizes: '60x60', href: '/static/icons/apple-icon-60x60.png' },
      { rel: 'apple-touch-icon', sizes: '72x72', href: '/static/icons/apple-icon-72x72.png' },
      { rel: 'apple-touch-icon', sizes: '76x76', href: '/static/icons/apple-icon-76x76.png' },
      { rel: 'apple-touch-icon', sizes: '114x114', href: '/static/icons/apple-icon-114x114.png' },
      { rel: 'apple-touch-icon', sizes: '120x120', href: '/static/icons/apple-icon-120x120.png' },
      { rel: 'apple-touch-icon', sizes: '144x144', href: '/static/icons/apple-icon-144x144.png' },
      { rel: 'apple-touch-icon', sizes: '152x152', href: '/static/icons/apple-icon-152x152.png' },
      { rel: 'apple-touch-icon', sizes: '180x180', href: '/static/icons/apple-icon-180x180.png' },
      { rel: 'icon', type: 'image/png', sizes: '192x192', href: '/static/icons/android-icon-192x192.png' },
      { rel: 'icon', type: 'image/png', sizes: '32x32', href: '/static/icons/favicon-32x32.png' },
      { rel: 'icon', type: 'image/png', sizes: '96x96', href: '/static/icons/favicon-96x96.png' },
      { rel: 'icon', type: 'image/png', sizes: '16x16', href: '/static/icons/favicon-16x16.png' },
    ],
    meta: [
      { name: 'msapplication-TileColor', content: '#263238' },
      { name: 'msapplication-TileImage', content: '/static/icons/ms-icon-144x144.png' },
      { name: 'theme-color', content: '#263238' }
    ]
  }
}
