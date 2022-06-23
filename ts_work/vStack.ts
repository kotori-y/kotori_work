// 将N个二维数组按照列拼接为一个二维数组
// concatenate n 2d-arrays to 1 array
export function vStack<T> (...array: Array<T>[][]): Array<T>[] {
  if (array.length === 1) {
    return array[0]
  }
  return array[0].map((elem, index) => {
    return elem.concat(...array.slice(1).map((value) => value[index]))
  })
}