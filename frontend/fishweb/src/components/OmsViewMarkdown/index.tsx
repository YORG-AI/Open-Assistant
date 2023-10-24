import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneLight } from 'react-syntax-highlighter/dist/esm/styles/prism';
type tProps = {
  textContent: string; // markdown文本
  // darkMode: string;
  //  a11yDark, atomDark, base16AteliersulphurpoolLight,
  //  cb, coldarkCold, coldarkDark, coy, coyWithoutShadows,
  //  darcula, dark, dracula, duotoneDark, duotoneEarth,
  //  duotoneForest, duotoneLight, duotoneSea, duotoneSpace,
  //   funky, ghcolors, gruvboxDark, gruvboxLight, holiTheme,
  //   hopscotch, lucario, materialDark, materialLight, materialOceanic,
  //   nightOwl, nord, okaidia, oneDark, oneLight, pojoaque, prism, shadesOfPurple,
  //   solarizedDarkAtom, solarizedlight, synthwave84, tomorrow, twilight, vs,
  //   vscDarkPlus, xonokai, zTouch
};

const OmsViewMarkdown: React.FC<tProps> = (props: tProps) => {
  const { textContent } = props;
  return (
    <ReactMarkdown
      components={{
        code({ node, className, children, ...props }) {
          const match = /language-(\w+)/.exec(className || '');
          return match ? (
            <SyntaxHighlighter
              showLineNumbers={true}
              style={oneLight}
              language={match[1]}
              PreTag="div"
              lineNumberStyle={{ color: '#000' }}
              {...props}
            >
              {String(children).replace(/\n$/, '')}
            </SyntaxHighlighter>
          ) : (
            <code className={className} {...props}>
              {children}
            </code>
          );
        },
      }}
    >
      {textContent}
    </ReactMarkdown>
  );
};

export default OmsViewMarkdown;
