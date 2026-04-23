package saxpathexception;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

public class SAXPathExceptionTest {

 @Test
 void testSAXPathExceptionString() {
 String msg = "test message";
 SAXPathException exception = new SAXPathException(msg);
 assertEquals(msg, exception.getMessage());
 }

 @Test
 void testSAXPathExceptionThrowable() {
 Throwable src = new Exception("source");
 SAXPathException exception = new SAXPathException(src);
 assertEquals(src, exception.getCause());
 assertEquals(src.getMessage(), exception.getMessage());
 }

 @Test
 void testGetCause() {
 Throwable src = new Exception("source");
 SAXPathException exception = new SAXPathException(src);
 assertEquals(src, exception.getCause());
 }
}