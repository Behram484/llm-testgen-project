package org.saxpath;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class SAXPathExceptionTest_v1 {
 
 @Test
 void testSAXPathExceptionString() {
 String message = "Test exception";
 SAXPathException ex = new SAXPathException(message);
 assertEquals(message, ex.getMessage());
 }

 @Test
 void testSAXPathExceptionThrowable() {
 Throwable src = new Exception("Source exception");
 String message = "Test exception";
 SAXPathException ex = new SAXPathException(src);
 assertEquals(message, ex.getMessage());
 assertSame(src, ex.getCause());
 }
}