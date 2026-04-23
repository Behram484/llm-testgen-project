package axis;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

public class AxisTest_v1 {
 @Test
 void testLookupWithValidAxisNum() {
 assertEquals("child", Axis.lookup(Axis.CHILD));
 assertEquals("descendant", Axis.lookup(Axis.DESCENDANT));
 // more tests...
 }

 @Test
 void testLookupWithInvalidAxisNum() {
 assertEquals(0, Axis.lookup("invalid axis"));
 }
}