import React, {type ReactNode} from 'react';
import Content from '@theme-original/DocItem/Content';
import type ContentType from '@theme/DocItem/Content';
import type {WrapperProps} from '@docusaurus/types';
import {useDoc} from '@docusaurus/plugin-content-docs/client';
import ModuleBanner, {getModuleInfo} from '@site/src/components/ModuleBanner';

type Props = WrapperProps<typeof ContentType>;

export default function ContentWrapper(props: Props): ReactNode {
  const {metadata} = useDoc();
  const moduleInfo = getModuleInfo(metadata.title);

  return (
    <>
      {moduleInfo && (
        <ModuleBanner
          moduleNumber={moduleInfo.moduleNumber}
          title={moduleInfo.moduleName}
          icon={moduleInfo.icon}
        />
      )}
      <Content {...props} />
    </>
  );
}
