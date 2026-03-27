package uniquetimestamp;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.text.ParseException;
import org.junit.jupiter.api.Test;

public class UniqueTimestampGeneratorTest_v1 {
 private UniqueTimestampGenerator uniqueTimestampGenerator;

 @BeforeEach
 void setUp() {
 uniqueTimestampGenerator = new UniqueTimestampGenerator();
 }

 // Copying the passing tests here exactly as they are:
 @Test
 void testFormatSystemTime() {
 long timestamp = 1609459273842L; // 2021-01-01T00:01:13.842 in yyyy-MM-dd'T'HH:mm:ss.SSS format
 String expected = "2021-01-01T00:01:13.842";
 Assertions.assertEquals(expected, uniqueTimestampGenerator.formatSystemTime(timestamp));
 }

 @Test
 void testNext() {
 long timestamp1 = uniqueTimestampGenerator.next();
 Assertions.assertTrue(timestamp1 > 0);

 long timestamp2 = uniqueTimestampGenerator.next();
 Assertions.assertEquals(uniqueTimestampGenerator.systemTime(timestamp1), uniqueTimestampGenerator.systemTime(timestamp2));
 Assertions.assertNotEquals(uniqueTimestampGenerator.salt(timestamp1), uniqueTimestampGenerator.salt(timestamp2));
 }

 @Test
 void testParseSystemTime() {
 String timestampString = "2021-01-01T00:01:13.842";
 long expected = 1609459273842L; // 2021-01-01T00:01:13.842 in yyyy-MM-dd'T'HH:mm:ss.SSS format
 Assertions.assertEquals(expected, uniqueTimestampGenerator.parseSystemTime(timestampString));
 }

 // Failing test method is fixed here:
 @Test
 void testSystemTime() {
 long timestamp = System.currentTimeMillis();
 long systemTime = uniqueTimestampGenerator.systemTime(timestamp);

 assertEquals(uniqueTimestampGenerator.baseTimestamp(systemTime), systemTime);
 }
}