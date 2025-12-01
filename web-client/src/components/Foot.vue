<template>
  <div class="foot">
    <footer>
      <p id="docs">
        <a
          href="https://enzyhtp.app.vanderbilt.edu/docs.html?doc=terms"
          target="_blank"
          ><span>Terms of Service</span></a
        >
        ·
        <a
          href="https://enzyhtp.app.vanderbilt.edu/docs.html?doc=privacy"
          target="_blank"
          ><span>Privacy Policy</span></a
        >
      </p>
      <p>© 2023-{{ year }}, Vanderbilt University. All Rights Reserved.</p>
    </footer>
  </div>
</template>
<script setup>
import { ref, reactive } from "vue";
const year = ref(new Date().getFullYear());

/**
 *
 */
</script>
<style lang="scss" scoped>
.foot {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  
}
p{
  margin-top: 6px;
}

footer {
  margin-top: 6vh;
  text-align: center;
}

footer > #docs > a {
  color: lightslategray;
  cursor: pointer;
}


@media screen and (max-width: 1200px) {
  #footer {
    margin-top: 6vh;
  }

  #footer > div > img {
    width: 10vw;
  }
}
</style>
