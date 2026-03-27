package calculator;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class CalculatorTest {
 private final Calculator calculator = new Calculator();

 @Test
 void testAdd() {
 assertEquals(5, calculator.add(2, 3));
 assertEquals(0, calculator.add(Integer.MAX_VALUE, Integer.MIN_VALUE + 1)); // This should fail due to overflow
 }

 @Test
 void testSubtract() {
 assertEquals(10, calculator.subtract(25, 15));
 assertEquals(-5, calculator.subtract(Integer.MAX_VALUE, Integer.MIN_VALUE + 4)); // This should pass now that the subtraction operation is correct
 }
}