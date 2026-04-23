package outputconfig;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import java.util.Properties;

public class OutputConfigTest_v1 {
 @Test
 public void testCreateOutputConfig() {
 Properties properties = new Properties();
 properties.setProperty("method", "xml");
 
 OutputConfig outputConfig = OutputConfig.createOutputConfig(properties)[43D[K
OutputConfig.createOutputConfig(properties);

 Assertions.assertEquals("xml", outputConfig.method, "Method should be '[1D[K
'xml'");
 Assertions.assertFalse(outputConfig.isXhtml, "isXhtml should be false")[7D[K
false");
 Assertions.assertFalse(outputConfig.isText, "isText should be false");
 Assertions.assertFalse(outputConfig.isHtml, "isHtml should be false");
 }
 
 @Test
 public void testCreateOutputConfigWithUnknownMethod() {
 Properties properties = new Properties();
 properties.setProperty("method", "unknown");
 
 Assertions.assertThrows(IllegalArgumentException.class, () -> OutputCon[9D[K
OutputConfig.createOutputConfig(properties));
 }
 
 @Test
 public void testCreateOutputConfigWithoutMethod() {
 Properties properties = new Properties();
 
 Assertions.assertThrows(IllegalArgumentException.class, () -> OutputCon[9D[K
OutputConfig.createOutputConfig(properties));
 }
}