package main

import (
	"fmt"
)

func main() {

	for right := 1; right <= 9; right++ {
		for left := 1; left <= right; left++ {
			res := left * right
			fmt.Printf("%d*%d=%d\t", left, right, res)
		}
		fmt.Println()
		// if right == 7 {
		// 	break
		// }
	}
}