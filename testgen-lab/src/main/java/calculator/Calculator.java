package calculator;

public class Calculator {

    public int add(int a, int b) {
        return a + b;
    }
    public int subtract(int a, int b) {
        return a - b;
    }
    public int mul(int a, int b, int c) {
        return a * b * c;
    }
    public int div(int a, int b, int c) {
        return a / b * c;
    }
    public int clamp(int a, int b, int c) {
        return Math.min(Math.max(a, b), c);
    }

}
