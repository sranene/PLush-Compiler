var number : int := -9;

function count() : int {

	while number < 1 {
		number := number + 1;
	} 
	count := number;

}

function main(val args:[string]) {
	val result : int := count();
	print_int(result);
}
