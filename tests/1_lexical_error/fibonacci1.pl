function createEmptyArray() : [int];

function main(val args:[string]) {
	val n : int := 10; # Número de termos na sequência Fibonacci

	var arrIterative : [int] := createEmptyArray();

	var i : int := 0;
	while i < n {
		arrIterative[i] := fibonacciIterative(i);
		i := i + 1;
	}

    print_int_array(arrIterative);

}

# Função para calcular o número Fibonacci de um determinado índice usando uma abordagem iterativa
function fibonacciIterative(val n:int) : int? {
    if n <= 1 {
        fibonacciIterative := n;
    }
    var fib1 : int := 0;
    var fib2 : int := 1;
    var fib : int := 0;

	var i : int := 2;
	while i <= n {
		fib := fib1 + fib2;
		fib1 := fib2;
		fib2 := fib;
		i := i + 1;
	}
    fibonacciIterative := fib;
}
