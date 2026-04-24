package com.liferay.portal.kernel.util;

import java.math.RoundingMode;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class BigDecimalUtilTest_v1 {
 
 private static final double DELTA = 0.00001;

 @Test
 void testAdd() {
 assertEquals(4.0, BigDecimalUtil.add(1.2, 2.8), DELTA);
 }

 @Test
 void testMultiply() {
 assertEquals(10.0, BigDecimalUtil.multiply(2.5, 4), DELTA);
 }

 @Test
 void testScale() {
 assertEquals(10.34687, BigDecimalUtil.scale(10.34687, 5, RoundingMode.HALF[17D[K
RoundingMode.HALF_UP), DELTA);
 }

 @Test
 void testSubtract() {
 assertEquals(-3.0, BigDecimalUtil.subtract(5.99, 2.99), DELTA);
 }
}