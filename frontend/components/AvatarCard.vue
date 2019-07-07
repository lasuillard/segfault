<template>
  <div style="border: 1px solid black;">
    <img :src="avatar.profile_image"/>
    <p>id: {{ avatar.id }}</p>
    <p>display_name: {{ avatar.display_name }}</p>
    <p>introduce_message: {{ avatar.introduce_message }}</p>
  </div>
</template>

<script>
export default {
  props: {
    avatar: Object
  }
}
</script>
