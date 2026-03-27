package bigdecimalutil;

import org.junit.jupiter.api.Test;
import java.math.RoundingMode;
import static org.junit.jupiter.api.Assertions.*;

public class BigDecimalUtilTest_v1 {

 @Test
 void testAdd() {
 double x = 0.123456789;
 double y = 0.987654321;
 assertEquals(1.11111111, BigDecimalUtil.add(x, y), 0.000000001);
 }

 @Test
 void testMultiply() {
 double x = 5.6;
 double y = -3.4;
 assertEquals(-19.04, BigDecimalUtil.multiply(x, y), 0.000000001);
 }

 @Test
 void testScale() {
 double x = 56789.12345;
 int scale = 2;
 assertEquals(56789.12, BigDecimalUtil.scale(x, scale, RoundingMode.HALF_UP), 0.000000001);
 }

 @Test
 void testSubtract() {
 double x = 56789.12345;
 double y = 12345.67890;
 assertEquals(44443.44455, BigDecimalUtil.subtract(x, y), 0.000000001);
 }
}