package uniquetimestamp;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

public class UniqueTimestampGeneratorTest_v1 {
 
 private final UniqueTimestampGenerator uniqueTimestampGenerator = new U[1D[K
UniqueTimestampGenerator();
 
 @Test
 void testNext() {
 long timestamp = System.currentTimeMillis();
 long nextTimestamp = uniqueTimestampGenerator.next(timestamp);
 
 assertEquals(uniqueTimestampGenerator.systemTime(nextTimestamp), ti[2D[K
timestamp, "System time should match");
 assertThrows(RuntimeException.class, () -> uniqueTimestampGenerator[24D[K
uniqueTimestampGenerator.next(Long.MAX_VALUE));
 }
 
 @Test
 void testSalt() {
 long timestamp = System.currentTimeMillis();
 long nextTimestamp = uniqueTimestampGenerator.next(timestamp);
 
 assertEquals(uniqueTimestampGenerator.salt(nextTimestamp), 0, "Salt[5D[K
"Salt should be zero for the first call to next");
 }
 
 @Test
 void testBaseTimestamp() {
 long systemTime = 1638524799000L; // Fri Aug 26 2022 15:03:19 GMT+0[5D[K
GMT+0000 (Coordinated Universal Time)
 
 assertEquals(uniqueTimestampGenerator.baseTimestamp(systemTime), 18[2D[K
18446744071562067968L, "Base timestamp should match");
 }
 
 @Test
 void testFormatSystemTime() {
 long systemTime = 1638524799000L; // Fri Aug 26 2022 15:03:19 GMT+0[5D[K
GMT+0000 (Coordinated Universal Time)
 
 assertEquals(uniqueTimestampGenerator.formatSystemTime(systemTime),[67D[K
assertEquals(uniqueTimestampGenerator.formatSystemTime(systemTime), "2022-0assertEquals(uniqueTimestampGenerator.formatSystemTime(systemTime),"2022-08-26T15:03:19.000", "Formatted system time should match");
 }
 
 @Test
 void testParseSystemTime() throws Exception {
 String systemTime = "2022-08-26T15:03:19.000";
 
 assertEquals(uniqueTimestampGenerator.parseSystemTime(systemTime), [K
1638524799000L, "Parsed system time should match");
 }
}