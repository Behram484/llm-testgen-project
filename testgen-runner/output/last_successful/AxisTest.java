package org.saxpath;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

public class AxisTest {
 @Test
 void testLookupWithValidAxisNum() {
 assertEquals("child", Axis.lookup(Axis.CHILD));
 assertEquals("descendant", Axis.lookup(Axis.DESCENDANT));
 // more tests...
 }

 @Test
 void testLookupWithInvalidAxisName() {
 assertEquals(0, Axis.lookup("invalid axis"));
 }
}