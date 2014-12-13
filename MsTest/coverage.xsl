<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:param name="low_coverage" select="60"/>
  <xsl:param name="ok_coverage" select="30"/>
<xsl:template match="/">
    <html>
    <body>
      <h1>This is the coverage report</h1>
      <h2> Assembly coverage</h2>
      <table style="width:640;border:2px solid black;">
          <tr>
            <td style="font-weight:bold">Assembly</td>
            <td style="text-align:right;font-weight:bold">Blocks not covered</td>
            <td style="text-align:right;font-weight:bold">% blocks not covered</td>
          </tr>
        <xsl:for-each select="//Module">
          <tr>
            <td>
              <xsl:value-of select="ModuleName"/>
            </td>
            <td style="text-align:right">
              <xsl:value-of select="BlocksNotCovered"/>
              of
              <xsl:value-of select="(BlocksCovered+BlocksNotCovered)"/>
            </td>
            <td>
              <xsl:variable name="pct" select="(BlocksNotCovered div (BlocksNotCovered + BlocksCovered))*100"/>
              <xsl:attribute name="style">
                text-align:right;
                <xsl:choose>
                  <xsl:when test="number($pct &gt;= $low_coverage)">background-color:red;</xsl:when>
                  <xsl:when test="number($pct &gt;= $ok_coverage)">background-color:yellow;</xsl:when>
                  <xsl:otherwise>background-color:green;</xsl:otherwise>
                </xsl:choose>
              </xsl:attribute>
              <xsl:value-of select="$pct"/>
            </td>
          </tr>
        </xsl:for-each>
        </table>
    </body>
    </html>
</xsl:template>
</xsl:stylesheet>