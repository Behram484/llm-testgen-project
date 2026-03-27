package saxpathexception;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class SAXPathExceptionTest {
 @Test
 void testConstructorWithString() {
 String msg = "test message";
 SAXPathException exception = new SAXPathException(msg);
 assertEquals(msg, exception.getMessage());
 }
 
 @Test
 void testConstructorWithThrowable() {
 Throwable src = new Exception("source exception");
 SAXPathException exception = new SAXPathException(src);
 assertEquals(src.getClass(), exception.getCause().getClass());
 assertEquals(src.getMessage(), exception.getCause().getMessage());
 }
 
 @Test
 void testGetCause() {
 Throwable src = new Exception("source exception");
 SAXPathException exception = new SAXPathException(src);
 assertSame(src, exception.getCause());
 }
}