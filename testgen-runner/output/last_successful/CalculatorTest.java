package calculator;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class CalculatorTest {
 private final Calculator calculator = new Calculator();

 @Test
 void testAdd() {
 assertEquals(5, calculator.add(2, 3));
 }

 @Test
 void testSubtract() {
 assertEquals(-1, calculator.subtract(0, 1));
 }
}