package rs.demsys.rst.ui.highlighting;

import org.eclipse.xtext.ui.editor.syntaxcoloring.DefaultAntlrTokenToAttributeIdMapper;

public class RstAntlrTokenToAttributeIdMapper extends
DefaultAntlrTokenToAttributeIdMapper {

	@Override
	protected String calculateId(String tokenName, int tokenType) {
		// TODO Auto-generated method stub
		
		String id = super.calculateId(tokenName, tokenType);
		
		if (id.equals("keyword")) {
			return id;
		}
		else {
			return null;	
		}
		
	}

}
