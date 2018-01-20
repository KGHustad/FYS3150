.PHONY: bench

bench: bench-c bench-go bench-julia

bench-c: c/bench_ising.x
	make -C c run-benchmark

bench-go: go/bench/bench
	make -C go run-benchmark

bench-julia: go/bench/bench
	make -C julia run-benchmark
