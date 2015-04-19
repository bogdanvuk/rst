package rs.demsys.rst.ui.highlighting;

import org.eclipse.xtext.ui.editor.syntaxcoloring.IHighlightingConfiguration;
import org.eclipse.xtext.ui.editor.syntaxcoloring.IHighlightingConfigurationAcceptor;
import org.eclipse.swt.SWT;
import org.eclipse.swt.graphics.RGB;
import org.eclipse.xtext.ui.editor.syntaxcoloring.*;
import org.eclipse.xtext.ui.editor.utils.TextStyle;
import static org.eclipse.swt.SWT.*;


public class RstHighlightingConfiguration extends DefaultHighlightingConfiguration
{
    public static final String DIRECTIVE = "Directive";
    public static final String DIRECTIVE_TYPE = "DirectiveType";
    public static final String ITALIC_TEXT = "Italic Text";
    public static final String BOLD_TEXT = "Bold Text";
    public static final String FILE_NAME = "File Name";
    public static final String HEADING = "Heading";
    public static final String[] ALL_STRINGS = { 
        DIRECTIVE,
        DIRECTIVE_TYPE,
        HEADING,
        BOLD_TEXT,
        ITALIC_TEXT,
        FILE_NAME
    };
    
    
    public void configure(IHighlightingConfigurationAcceptor acceptor) {
    	addType( acceptor, KEYWORD_ID, 127, 0, 85, BOLD );
        addType( acceptor, DIRECTIVE, 50, 0, 0, NORMAL );
        addType( acceptor, DIRECTIVE_TYPE, 50, 0, 0, NORMAL );
        addType( acceptor, HEADING, 50, 0, 0, BOLD);
        addType( acceptor, ITALIC_TEXT, 50, 0, 0, ITALIC);
        addType( acceptor, BOLD_TEXT, 50, 0, 0, BOLD);
        addType( acceptor, FILE_NAME, 50, 0, 0, UNDERLINE_LINK);
    }
    
    public void addType( IHighlightingConfigurationAcceptor acceptor, String s, int r, int g, int b, int style )
    {
    	TextStyle textStyle = defaultTextStyle().copy();
        textStyle.setBackgroundColor(new RGB(255, 255, 255));
        textStyle.setColor(new RGB(r, g, b));
        textStyle.setStyle(style);
        acceptor.acceptDefaultHighlighting(s, s, textStyle);
    }
} 