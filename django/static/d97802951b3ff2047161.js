(window.webpackJsonp=window.webpackJsonp||[]).push([[4],{822:function(t,e,r){"use strict";r.r(e);r(12),r(9),r(6),r(5),r(10),r(44);var n=r(2),c=r(37);function o(object,t){var e=Object.keys(object);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(object);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(object,t).enumerable}))),e.push.apply(e,r)}return e}function l(t){for(var i=1;i<arguments.length;i++){var source=null!=arguments[i]?arguments[i]:{};i%2?o(source,!0).forEach((function(e){Object(n.a)(t,e,source[e])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(source)):o(source).forEach((function(e){Object.defineProperty(t,e,Object.getOwnPropertyDescriptor(source,e))}))}return t}var f={layout:"empty",methods:l({},Object(c.b)({_callback:"user/finishSocialLogin"})),created:function(){var t=this;this._callback(l({},this.$route.query)).then((function(e){t.$router.replace({name:"index"})})).catch((function(t){throw Error(t)}))}},h=r(32),O=r(64),y=r.n(O),w=r(342),j=r(343),v=r(341),component=Object(h.a)(f,(function(){var t=this.$createElement,e=this._self._c||t;return e("v-container",{attrs:{fluid:""}},[e("v-flex",{attrs:{xs12:""}},[e("v-layout",{attrs:{"align-center":"","justify-center":"","fill-height":""}},[e("p",[this._v("Processing login... please wait")])])],1)],1)}),[],!1,null,null,null);e.default=component.exports;y()(component,{VContainer:w.a,VFlex:j.a,VLayout:v.a})}}]);