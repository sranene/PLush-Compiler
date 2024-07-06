val final_number : int := 16; #numero final

function fizzBuzz(val number:int) {
	var temp : int := 1;
	while temp <= "number" {
		if temp % 3 = 0 && temp % 5 = 0 {
			print_string("FizzBuzz");
		} else {
			if temp % 3 = 0 {
				print_string("Fizz");
			} else {
				if temp % 5 = 0 {
					print_string("Buzz");
				} else {
					print_int(temp);
				}
			}
		}
		temp := temp + 1;
	}
}


function main(val args:[string]) {
	fizzBuzz(final_number); #chamar a funcao
}
