<!--template>
    <v-container>
      <h2>Editor</h2>
      <div style="margin-top: 50px; margin-bottom: 50px;">
      <editor v-model="editorText" />
      </div>
      <h2>Preview</h2>
      <div style="margin-top: 50px; outline: 2px solid grey; padding: 10px">
        <viewer :value="editorText" />
      </div>

  </v-container>
</template>
<script>

import { Editor, Viewer } from '@toast-ui/vue-editor'
import 'tui-editor/dist/tui-editor.css';
import 'tui-editor/dist/tui-editor-contents.css';
import 'codemirror/lib/codemirror.css';

export default {

    components: {
      'editor': Editor,
      'viewer': Viewer
    },
    data() {
        return {
          editorText: "Enter Here",
        };
    },
};
</script-->
<template>
  <v-card light flex-column>
<!-- 뷰어 부분 -->
<v-card-title text>Making Fragment</v-card-title>
    <v-card-text>
      <p>Fragment 미리보기</p>
      <v-divider></v-divider>
      <viewer :value="editorText" />
      <v-divider></v-divider>
    </v-card-text>
  <editor v-model="editorText"/>
  <div style="margin-top: 20px;">

    <!--분류 설정 넣기-->

    <v-btn text color="primary">Done</v-btn>
  </div>
</v-card>

</template>

<script>

import { Editor, Viewer } from '@toast-ui/vue-editor'
import 'tui-editor/dist/tui-editor.css';
import 'tui-editor/dist/tui-editor-contents.css';
import 'codemirror/lib/codemirror.css';

export default {

    components: {
      'editor': Editor,
      'viewer': Viewer
    },
    data() {
        return {
          editorText: "",
        };
    },
};
</script>

<style>

</style>


<!-- 에디터 부분 -->
    <!-- <v-textarea
      label="내용"
      persistent-hint
      required
      v-model="form.content"
    ></v-textarea> -->