export const textContent = `
~~~python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Provide configuration, singleton
"""
import os
import openai
import yaml
from metagpt.const import PROJECT_ROOT
from metagpt.logs import logger
from metagpt.tools import SearchEngineType, WebBrowserEngineType
from metagpt.utils.singleton import Singleton
class NotConfiguredException(Exception):
    """Exception raised for errors in the configuration.
    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message="The required configuration is not set"):
        self.message = message
        super().__init__(self.message)
class Config(metaclass=Singleton):
    """
    Regular usage method:
    config = Config("config.yaml")
    secret_key = config.get_key("MY_SECRET_KEY")
    print("Secret key:", secret_key)
    """
    _instance = None
    key_yaml_file = PROJECT_ROOT / "config/key.yaml"
    default_yaml_file = PROJECT_ROOT / "config/config.yaml"
    def __init__(self, yaml_file=default_yaml_file):
        self._configs = {}
        self._init_with_config_files_and_env(self._configs, yaml_file)
        logger.info("Config loading done.")
        self.global_proxy = self._get("GLOBAL_PROXY")
        self.openai_api_key = self._get("OPENAI_API_KEY")
        self.anthropic_api_key = self._get("Anthropic_API_KEY")
        if (not self.openai_api_key or "YOUR_API_KEY" == self.openai_api_key) and (
            not self.anthropic_api_key or "YOUR_API_KEY" == self.anthropic_api_key
        ):
            raise NotConfiguredException("Set OPENAI_API_KEY or Anthropic_API_KEY first")
        self.openai_api_base = self._get("OPENAI_API_BASE")
        openai_proxy = self._get("OPENAI_PROXY") or self.global_proxy
        if openai_proxy:
            openai.proxy = openai_proxy
~~~
`;

export const markdown = `
## 铜缆通信（续）
- 铜缆传输的编码和调制
- 铜缆的传输距离和衰减
- 铜缆的干扰和防护

## 无线通信
- 无线电波传输
- 微波传输
- 红外线传输
- 激光传输
- 无线传输的编码和调制
- 无线传输的传输距离和衰减

## 物理层故障排除
- 物理层故障的诊断方法
- 物理层故障的常见原因
- 物理层故障的排查工具

## 物理层性能优化
- 带宽利用率优化
- 信号质量优化
- 传输距离优化
- 抗干扰性能优化

## 其他相关主题
- 信道特性和传输媒介选择
- 数据传输的可靠性和效率
- 物理层与数据链路层的关系
- 物理层与网络层的交互
- 物理层的发展趋势


`;

export const markdown2 = `
# Step 1: Summary of Data

1. Load the dataset and display the first few rows to get a feel for the data.
2. Provide descriptive statistics (mean, median, standard deviation, minimum, maximum, etc.) for weight loss for each diet (A, B, C).
3. Visualize the data:
    - Create boxplots or histograms to show the distribution of weight loss for each diet.
    - Produce a bar chart to show average weight loss across the three diets.
4. Check for any missing values in the dataset and decide on how to handle them (e.g., remove or impute).

---

# Step 2: Diagnostics

1. Check the assumptions for ANOVA:
    - **Normality**: Use Shapiro-Wilk test or QQ plots to test if weight loss for each diet follows a normal distribution.
    - **Homogeneity of variances**: Use Levene's test or Bartlett's test to see if the variances of weight losses are the same across the three diets.
2. If assumptions are violated, decide on remedies:
    - Transformations for normality.
    - If variances are significantly different, consider using Welch's ANOVA.

---

# Step 3: Model Fitting

1. Fit an ANOVA model to analyze the differences in weight loss across the three diets.


`;
