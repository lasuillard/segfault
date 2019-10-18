<template>
    <v-card>
        <v-card-subtitle>Fragment Title</v-card-subtitle>
        <v-divider />
            <div>
            <viewer :value="FrgText" />
            </div>

            <div>
            <AnswerForm></AnswerForm>
            </div>
    </v-card>
</template>

<script>

import { Editor, Viewer } from '@toast-ui/vue-editor'
import 'tui-editor/dist/tui-editor.css';
import 'tui-editor/dist/tui-editor-contents.css';
import 'codemirror/lib/codemirror.css';

import AnswerForm from '~/components/AnswerForm.vue'

export default {
    data() {
        return {
          FrgText: "### This is my docker Problem1 \n ## Actually I'm in first time to use docker",
          content: ""
        };
    },
    components: {
      'editor': Editor,
      'viewer': Viewer,
      'AnswerForm': AnswerForm,
    },
}
</script>

<style>

</style>
