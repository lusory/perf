use rand::{thread_rng, Rng};
use std::time::Instant;

const n: i32 = 2048;

fn main() {
    let mut rng = thread_rng();
    let mut a: Vec<Vec<f64>> = vec![vec![0.0; n]; n];
    let mut b: Vec<Vec<f64>> = vec![vec![0.0; n]; n];
    let mut c: Vec<Vec<f64>> = vec![vec![0.0; n]; n];
    
    for i in 0..n {
        for j in 0..n {
            a[i][j] = rng.gen::<f64>();
            b[i][j] = rng.gen::<f64>();
        }
    }
    
    let nw = Instant::now();
    
    for i in 0..n {
        for j in 0..n {
            for k in 0..n {
                c[i][j] += a[i][k] * b[k][j];
            }
        }
    }
    
    println!("{}", nw.elapsed().as_secs());
}