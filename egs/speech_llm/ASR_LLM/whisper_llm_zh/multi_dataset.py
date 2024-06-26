# Copyright      2023  Xiaomi Corp.        (authors: Zengrui Jin)
#
# See ../../../../LICENSE for clarification regarding multiple authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import glob
import logging
import re
from pathlib import Path
from typing import Dict, List

import lhotse
from lhotse import CutSet, load_manifest_lazy


class MultiDataset:
    def __init__(self, fbank_dir: str):
        """
        Args:
          manifest_dir:
            It is expected to contain the following files:
            - aishell_cuts_train.jsonl.gz
            - aishell2_cuts_train.jsonl.gz
            - aishell4_cuts_train_L.jsonl.gz
            - aishell4_cuts_train_M.jsonl.gz
            - aishell4_cuts_train_S.jsonl.gz
            - alimeeting-far_cuts_train.jsonl.gz
            - magicdata_cuts_train.jsonl.gz
            - primewords_cuts_train.jsonl.gz
            - stcmds_cuts_train.jsonl.gz
            - thchs_30_cuts_train.jsonl.gz
            - kespeech/kespeech-asr_cuts_train_phase1.jsonl.gz
            - kespeech/kespeech-asr_cuts_train_phase2.jsonl.gz
            - wenetspeech/cuts_L_fixed.jsonl.gz
        """
        self.fbank_dir = Path(fbank_dir)

    def train_cuts(self) -> CutSet:
        logging.info("About to get multidataset train cuts")

        # THCHS-30
        logging.info("Loading THCHS-30 in lazy mode")
        thchs_30_cuts = load_manifest_lazy(
            self.fbank_dir / "thchs_30_cuts_train.jsonl.gz"
        )

        # AISHELL-1
        logging.info("Loading Aishell-1 in lazy mode")
        aishell_cuts = load_manifest_lazy(
            self.fbank_dir / "aishell_cuts_train.jsonl.gz"
        )

        # AISHELL-2
        logging.info("Loading Aishell-2 in lazy mode")
        aishell_2_cuts = load_manifest_lazy(
            self.fbank_dir / "aishell2_cuts_train.jsonl.gz"
        )

        # AISHELL-4
        logging.info("Loading Aishell-4 in lazy mode")
        aishell_4_L_cuts = load_manifest_lazy(
            self.fbank_dir / "aishell4_cuts_train_L.jsonl.gz"
        )
        aishell_4_M_cuts = load_manifest_lazy(
            self.fbank_dir / "aishell4_cuts_train_M.jsonl.gz"
        )
        aishell_4_S_cuts = load_manifest_lazy(
            self.fbank_dir / "aishell4_cuts_train_S.jsonl.gz"
        )

        # ST-CMDS
        logging.info("Loading ST-CMDS in lazy mode")
        stcmds_cuts = load_manifest_lazy(self.fbank_dir / "stcmds_cuts_train.jsonl.gz")

        # Primewords
        logging.info("Loading Primewords in lazy mode")
        primewords_cuts = load_manifest_lazy(
            self.fbank_dir / "primewords_cuts_train.jsonl.gz"
        )

        # MagicData
        logging.info("Loading MagicData in lazy mode")
        magicdata_cuts = load_manifest_lazy(
            self.fbank_dir / "magicdata_cuts_train.jsonl.gz"
        )

        # Ali-Meeting
        logging.info("Loading Ali-Meeting in lazy mode")
        alimeeting_cuts = load_manifest_lazy(
            self.fbank_dir / "alimeeting-far_cuts_train.jsonl.gz"
        )

        # WeNetSpeech
        logging.info("Loading WeNetSpeech in lazy mode")
        wenetspeech_L_cuts = load_manifest_lazy(
            self.fbank_dir / "wenetspeech" / "cuts_L_fixed.jsonl.gz"
        )

        # KeSpeech
        logging.info("Loading KeSpeech in lazy mode")
        kespeech_1_cuts = load_manifest_lazy(
            self.fbank_dir / "kespeech" / "kespeech-asr_cuts_train_phase1.jsonl.gz"
        )
        kespeech_2_cuts = load_manifest_lazy(
            self.fbank_dir / "kespeech" / "kespeech-asr_cuts_train_phase2.jsonl.gz"
        )

        return CutSet.mux(
            thchs_30_cuts,
            aishell_cuts,
            aishell_2_cuts,
            aishell_4_L_cuts,
            aishell_4_M_cuts,
            aishell_4_S_cuts,
            alimeeting_cuts,
            stcmds_cuts,
            primewords_cuts,
            magicdata_cuts,
            wenetspeech_L_cuts,
            kespeech_1_cuts,
            kespeech_2_cuts,
            weights=[
                len(thchs_30_cuts),
                len(aishell_cuts),
                len(aishell_2_cuts),
                len(aishell_4_L_cuts),
                len(aishell_4_M_cuts),
                len(aishell_4_S_cuts),
                len(alimeeting_cuts),
                len(stcmds_cuts),
                len(primewords_cuts),
                len(magicdata_cuts),
                len(wenetspeech_L_cuts),
                len(kespeech_1_cuts),
                len(kespeech_2_cuts),
            ],
        )

    def dev_cuts(self) -> CutSet:
        logging.info("About to get multidataset dev cuts")

        # WeNetSpeech
        logging.info("Loading WeNetSpeech DEV set in lazy mode")
        wenetspeech_dev_cuts = load_manifest_lazy(
            self.fbank_dir / "wenetspeech" / "cuts_DEV_fixed.jsonl.gz"
        )

        return wenetspeech_dev_cuts

    def test_cuts(self) -> Dict[str, CutSet]:
        logging.info("About to get multidataset test cuts")

        # AISHELL
        logging.info("Loading Aishell set in lazy mode")
        aishell_test_cuts = load_manifest_lazy(
            self.fbank_dir / "aishell_cuts_test.jsonl.gz"
        )
        aishell_dev_cuts = load_manifest_lazy(
            self.fbank_dir / "aishell_cuts_dev.jsonl.gz"
        )

        # AISHELL-2
        logging.info("Loading Aishell-2 set in lazy mode")
        aishell2_test_cuts = load_manifest_lazy(
            self.fbank_dir / "aishell2_cuts_test.jsonl.gz"
        )
        aishell2_dev_cuts = load_manifest_lazy(
            self.fbank_dir / "aishell2_cuts_dev.jsonl.gz"
        )

        # AISHELL-4
        logging.info("Loading Aishell-4 TEST set in lazy mode")
        aishell4_test_cuts = load_manifest_lazy(
            self.fbank_dir / "aishell4_cuts_test.jsonl.gz"
        )

        # Ali-Meeting
        logging.info("Loading Ali-Meeting set in lazy mode")
        alimeeting_test_cuts = load_manifest_lazy(
            self.fbank_dir / "alimeeting-far_cuts_test.jsonl.gz"
        )
        alimeeting_eval_cuts = load_manifest_lazy(
            self.fbank_dir / "alimeeting-far_cuts_eval.jsonl.gz"
        )

        # MagicData
        logging.info("Loading MagicData set in lazy mode")
        magicdata_test_cuts = load_manifest_lazy(
            self.fbank_dir / "magicdata_cuts_test.jsonl.gz"
        )
        magicdata_dev_cuts = load_manifest_lazy(
            self.fbank_dir / "magicdata_cuts_dev.jsonl.gz"
        )

        # KeSpeech
        logging.info("Loading KeSpeech set in lazy mode")
        kespeech_test_cuts = load_manifest_lazy(
            self.fbank_dir / "kespeech" / "kespeech-asr_cuts_test.jsonl.gz"
        )
        kespeech_dev_phase1_cuts = load_manifest_lazy(
            self.fbank_dir / "kespeech" / "kespeech-asr_cuts_dev_phase1.jsonl.gz"
        )
        kespeech_dev_phase2_cuts = load_manifest_lazy(
            self.fbank_dir / "kespeech" / "kespeech-asr_cuts_dev_phase2.jsonl.gz"
        )

        # WeNetSpeech
        logging.info("Loading WeNetSpeech set in lazy mode")
        wenetspeech_test_meeting_cuts = load_manifest_lazy(
            self.fbank_dir / "wenetspeech" / "cuts_TEST_MEETING.jsonl.gz"
        )
        wenetspeech_test_net_cuts = load_manifest_lazy(
            self.fbank_dir / "wenetspeech" / "cuts_TEST_NET.jsonl.gz"
        )
        wenetspeech_dev_cuts = load_manifest_lazy(
            self.fbank_dir / "wenetspeech" / "cuts_DEV_fixed.jsonl.gz"
        )

        return {
            "wenetspeech-meeting_test": wenetspeech_test_meeting_cuts,
            "aishell_test": aishell_test_cuts,
            "aishell_dev": aishell_dev_cuts,
            "ali-meeting_test": alimeeting_test_cuts,
            "ali-meeting_eval": alimeeting_eval_cuts,
            "aishell-4_test": aishell4_test_cuts,
            "aishell-2_test": aishell2_test_cuts,
            "aishell-2_dev": aishell2_dev_cuts,
            "magicdata_test": magicdata_test_cuts,
            "magicdata_dev": magicdata_dev_cuts,
            "kespeech-asr_test": kespeech_test_cuts,
            "kespeech-asr_dev_phase1": kespeech_dev_phase1_cuts,
            "kespeech-asr_dev_phase2": kespeech_dev_phase2_cuts,
            "wenetspeech-net_test": wenetspeech_test_net_cuts,
            "wenetspeech_dev": wenetspeech_dev_cuts,
        }

    def aishell_train_cuts(self) -> CutSet:
        logging.info("About to get multidataset train cuts")
        logging.info("Loading Aishell-1 in lazy mode")
        aishell_cuts = load_manifest_lazy(
            self.fbank_dir / "aishell_cuts_train.jsonl.gz"
        )

        return aishell_cuts

    def aishell_dev_cuts(self) -> CutSet:
        logging.info("About to get multidataset dev cuts")
        logging.info("Loading Aishell set in lazy mode")
        aishell_dev_cuts = load_manifest_lazy(
            self.fbank_dir / "aishell_cuts_dev.jsonl.gz"
        )

        return aishell_dev_cuts

    def aishell_test_cuts(self) -> CutSet:
        logging.info("About to get multidataset test cuts")
        logging.info("Loading Aishell set in lazy mode")
        aishell_test_cuts = load_manifest_lazy(
            self.fbank_dir / "aishell_cuts_test.jsonl.gz"
        )

        return {
            "aishell_test": aishell_test_cuts,
        }

    def aishell2_train_cuts(self) -> CutSet:
        logging.info("About to get multidataset train cuts")
        logging.info("Loading Aishell-2 in lazy mode")
        aishell_2_cuts = load_manifest_lazy(
            self.fbank_dir / "aishell2_cuts_train.jsonl.gz"
        )

        return aishell_2_cuts

    def aishell2_dev_cuts(self) -> CutSet:
        logging.info("About to get multidataset dev cuts")
        logging.info("Loading Aishell-2 set in lazy mode")
        aishell2_dev_cuts = load_manifest_lazy(
            self.fbank_dir / "aishell2_cuts_dev.jsonl.gz"
        )

        return aishell2_dev_cuts

    def aishell2_test_cuts(self) -> CutSet:
        logging.info("About to get multidataset test cuts")
        logging.info("Loading Aishell-2 set in lazy mode")
        aishell2_test_cuts = load_manifest_lazy(
            self.fbank_dir / "aishell2_cuts_test.jsonl.gz"
        )

        return {
            "aishell2_test": aishell2_test_cuts,
        }

    def wenetspeech_test_meeting_cuts(self) -> CutSet:
        logging.info("About to get multidataset test cuts")
        logging.info("Loading WeNetSpeech set in lazy mode")
        wenetspeech_test_meeting_cuts = load_manifest_lazy(
            self.fbank_dir / "wenetspeech" / "cuts_TEST_MEETING.jsonl.gz"
        )

        return {
            "wenetspeech-meeting_test": wenetspeech_test_meeting_cuts,
        }

    def speechio_test_cuts(self) -> Dict[str, CutSet]:
        logging.info("About to get multidataset test cuts")
        start_index = 0
        end_index = 26
        dataset_parts = []
        for i in range(start_index, end_index + 1):
            idx = f"{i}".zfill(2)
            dataset_parts.append(f"SPEECHIO_ASR_ZH000{idx}")

        prefix = "speechio"
        suffix = "jsonl.gz"

        results_dict = {}
        for partition in dataset_parts:
            path = f"{prefix}_cuts_{partition}.{suffix}"

            logging.info(f"Loading {path} set in lazy mode")
            test_cuts = load_manifest_lazy(self.fbank_dir / path)
            results_dict[partition] = test_cuts

        return results_dict
