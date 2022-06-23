// 将一个1d-array转成 m*n 的2d-array
// convert a 1d-array to m*n 2d-array
export function reshape<T> (array: Array<T>, row: number, col: number): Array<Array<T>> | null {
  if (array.length === row * col) {
    return Array(row).fill(0).map((elem, index) => {
      const left = index * col
      const right = left + col
      return array.slice(left, right)
    })
  }
  return null
}