/*
 * @Description: implement sleep-like of python in JS
 * @Author: Kotori Y
 * @Date: 2020-12-30 13:48:26
 * @LastEditors: Kotori Y
 * @LastEditTime: 2020-12-30 14:04:55
 * @FilePath: \lib\sleep.js
 * @AuthorMail: kotori@cbdd.me
 */

const timer = (ms) => new Promise((res) => setTimeout(res, ms));

async function sleepTest (cond) {
  if (cond) {
    for (var i = 1; i <= 10; i++) {
      console.log(i); // do somwthing
      await timer(0.1*1000) // stop 0.1s
    }
  }
}

sleepTest(false)


// export default { timer }
module.exports = { timer }