val number : int := 99;

function assign() : int {
	var temp : int := 0;
	temp := number;
	assign := temp;
}

function main(val args:[string]) {
	val result : int := assign();
	print_int(result);
}