package com.ib.client;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

public class UtilTest_v1 {
 @Test
 public void testStringIsEmpty() {
 assertEquals(true, Util.StringIsEmpty(""));
 assertEquals(false, Util.StringIsEmpty("Hello World"));
 }
 
 @Test
 public void testNormalizeString() {
 assertEquals("", Util.NormalizeString(null));
 assertEquals("Hello World", Util.NormalizeString("Hello World"));
 }
}