use std::time::{SystemTime, Instant, UNIX_EPOCH};

const N: usize = 2048;

// minimal crate-free Xorshift 128 random number generator

const KX: u32 = 123456789;
const KY: u32 = 362436069;
const KZ: u32 = 521288629;
const KW: u32 = 88675123;

pub struct Rand {
    x: u32,
    y: u32,
    z: u32,
    w: u32,
}

impl Rand {
    pub fn new(seed: u32) -> Rand {
        Rand {
            x: KX ^ seed,
            y: KY ^ seed,
            z: KZ,
            w: KW,
        }
    }

    pub fn rand(&mut self) -> u32 {
        let t = self.x ^ self.x.wrapping_shl(11);
        self.x = self.y;
        self.y = self.z;
        self.z = self.w;
        self.w ^= self.w.wrapping_shr(19) ^ t ^ t.wrapping_shr(8);
        return self.w;
    }

    pub fn rand_float(&mut self) -> f64 {
        (self.rand() as f64) / (<u32>::max_value() as f64)
    }
}

fn main() {
    let mut rng = Rand::new(SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_secs_f32() as u32);
    let mut a: Vec<Vec<f64>> = vec![vec![0.0; N]; N];
    let mut b: Vec<Vec<f64>> = vec![vec![0.0; N]; N];
    let mut c: Vec<Vec<f64>> = vec![vec![0.0; N]; N];

    for i in 0..N {
        for j in 0..N {
            a[i][j] = rng.rand_float();
            b[i][j] = rng.rand_float();
        }
    }

    let nw = Instant::now();

    for i in 0..N {
        for j in 0..N {
            for k in 0..N {
                c[i][j] += a[i][k] * b[k][j];
            }
        }
    }

    println!("{}", nw.elapsed().as_secs());
}
