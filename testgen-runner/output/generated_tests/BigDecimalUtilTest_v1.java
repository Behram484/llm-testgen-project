package bigdecimalutil;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.math.RoundingMode;

public class BigDecimalUtilTest_v1 {

 @Test
 void testAdd() {
 double result = BigDecimalUtil.add(0.5, 2);
 assertEquals(2.5, result, () -> "Addition of two numbers should work");[7D[K
work");
 }

 @Test
 void testMultiply() {
 double result = BigDecimalUtil.multiply(10.0, 3);
 assertEquals(30.0, result, () -> "Multiplication of two numbers should [K
work");
 }

 @Test
 void testScale() {
 double result = BigDecimalUtil.scale(25.478963, 2, RoundingMode.HALF_UP[20D[K
RoundingMode.HALF_UP);
 assertEquals(25.48, result, () -> "Scaling of a number should work");
 }

 @Test
 void testSubtract() {
 double result = BigDecimalUtil.subtract(10.5, 3.2);
 assertEquals(7.3, result, () -> "Subtraction of two numbers should work[4D[K
work");
 }
}