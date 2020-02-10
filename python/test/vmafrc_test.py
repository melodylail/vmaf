from __future__ import absolute_import

import unittest

from vmaf.config import VmafConfig
from vmaf.core.asset import Asset
from vmaf.core.quality_runner import VmafrcQualityRunner, VmafossExecQualityRunner
from vmaf.core.result_store import FileSystemResultStore
from .testutil import set_default_576_324_videos_for_testing

__copyright__ = "Copyright 2016-2019, Netflix, Inc."
__license__ = "Apache, Version 2.0"


class VmafrcQualityRunnerTest(unittest.TestCase):

    def tearDown(self):
        if hasattr(self, 'runner'):
            self.runner.remove_results()
            pass

    def setUp(self):
        self.result_store = FileSystemResultStore()

    def test_run_vmafrc_runner_matched_to_vmafossexec(self):

        ref_path, dis_path, asset, asset_original = set_default_576_324_videos_for_testing()

        self.runner = VmafrcQualityRunner(
            [asset, asset_original],
            None, fifo_mode=True,
            delete_workdir=True,
            result_store=None,
            optional_dict={
                'psnr': True,
                'ssim': True,
                'ms_ssim': True,
            }
        )
        self.runner.run(parallelize=True)

        results = self.runner.results

        self.assertAlmostEqual(results[0]['VMAFRC_vif_scale0_score'],0.3634208125, places=8)
        self.assertAlmostEqual(results[0]['VMAFRC_vif_scale1_score'], 0.7666474166666667, places=8)
        self.assertAlmostEqual(results[0]['VMAFRC_vif_scale2_score'], 0.8628533333333334, places=5)
        self.assertAlmostEqual(results[0]['VMAFRC_vif_scale3_score'], 0.9159719583333334, places=8)
        self.assertAlmostEqual(results[0]['VMAFRC_motion2_score'], 3.895352291666667, places=8)
        self.assertAlmostEqual(results[0]['VMAFRC_adm2_score'], 0.9345877291666667, places=8)
        self.assertAlmostEqual(results[0]['VMAFRC_float_psnr_score'], 30.7550666667, places=8)
        self.assertAlmostEqual(results[0]['VMAFRC_float_ssim_score'], 0.86322654166666657, places=8)
        self.assertAlmostEqual(results[0]['VMAFRC_float_ms_ssim_score'], 0.9632406874999999, places=8)

        self.assertAlmostEqual(results[1]['VMAFRC_vif_scale0_score'], 1.0, places=8)
        self.assertAlmostEqual(results[1]['VMAFRC_vif_scale1_score'],0.9999998541666666, places=8)
        self.assertAlmostEqual(results[1]['VMAFRC_vif_scale2_score'],0.9999996041666667, places=8)
        self.assertAlmostEqual(results[1]['VMAFRC_vif_scale3_score'], 0.9999991458333334, places=8)
        self.assertAlmostEqual(results[1]['VMAFRC_motion2_score'], 3.895352291666667, places=8)
        self.assertAlmostEqual(results[1]['VMAFRC_adm2_score'], 1.0, places=8)
        self.assertAlmostEqual(results[1]['VMAFRC_float_psnr_score'], 60.0, places=8)
        self.assertAlmostEqual(results[1]['VMAFRC_float_ssim_score'], 1.0, places=8)
        self.assertAlmostEqual(results[1]['VMAFRC_float_ms_ssim_score'], 1.0, places=8)

        self.assertAlmostEqual(results[0]['VMAFRC_score'], 76.69926875, places=8)
        self.assertAlmostEqual(results[1]['VMAFRC_score'], 99.94641666666666, places=8)

    def test_run_vmafrc_runner_fixed_psnr_ssim(self):

        ref_path, dis_path, asset, asset_original = set_default_576_324_videos_for_testing()

        self.runner = VmafrcQualityRunner(
            [asset, asset_original],
            None, fifo_mode=True,
            delete_workdir=True,
            result_store=None,
            optional_dict={
                'fixed_psnr': True,
                'fixed_ssim': True,
                'fixed_ms_ssim': False,  # TODO: enable fixed_ms_ssim
                'no_prediction': True,
            }
        )
        self.runner.run(parallelize=True)

        results = self.runner.results

        self.assertAlmostEqual(results[0]['VMAFRC_psnr_y_score'], 30.755063979166668, places=8)
        self.assertAlmostEqual(results[0]['VMAFRC_psnr_cb_score'], 38.4494410625, places=8)
        self.assertAlmostEqual(results[0]['VMAFRC_psnr_cr_score'], 40.99191027083334, places=8)
        self.assertAlmostEqual(results[0]['VMAFRC_ssim_score'], 0.8613860416666667, places=8)

        self.assertAlmostEqual(results[1]['VMAFRC_psnr_y_score'], 60.0, places=8)
        self.assertAlmostEqual(results[1]['VMAFRC_psnr_cb_score'], 60.0, places=8)
        self.assertAlmostEqual(results[1]['VMAFRC_psnr_cr_score'], 60.0, places=8)
        self.assertAlmostEqual(results[1]['VMAFRC_ssim_score'], 1.0, places=8)

    def test_run_vmafrc_runner_yuv422p10le(self):

        ref_path = VmafConfig.test_resource_path("yuv", "src01_hrc00_576x324.yuv422p10le.yuv")
        dis_path = VmafConfig.test_resource_path("yuv", "src01_hrc01_576x324.yuv422p10le.yuv")
        asset = Asset(dataset="test", content_id=0, asset_id=0,
                      workdir_root=VmafConfig.workdir_path(),
                      ref_path=ref_path,
                      dis_path=dis_path,
                      asset_dict={'width': 576, 'height': 324,
                                  'yuv_type': 'yuv422p10le'})

        asset_original = Asset(dataset="test", content_id=0, asset_id=1,
                      workdir_root=VmafConfig.workdir_path(),
                      ref_path=ref_path,
                      dis_path=ref_path,
                      asset_dict={'width': 576, 'height': 324,
                                  'yuv_type': 'yuv422p10le'})

        self.runner = VmafrcQualityRunner(
            [asset, asset_original],
            None, fifo_mode=True,
            delete_workdir=True,
            result_store=None,
            optional_dict={
                'psnr': True,
                'ssim': True,
                'ms_ssim': True,
            }
        )
        self.runner.run()

        results = self.runner.results

        self.assertAlmostEqual(results[0]['VMAFRC_vif_scale0_score'],0.3634208125, places=8)
        self.assertAlmostEqual(results[0]['VMAFRC_vif_scale1_score'], 0.7666474166666667, places=8)
        self.assertAlmostEqual(results[0]['VMAFRC_vif_scale2_score'], 0.8628533333333334, places=8)
        self.assertAlmostEqual(results[0]['VMAFRC_vif_scale3_score'], 0.9159719583333334, places=8)
        self.assertAlmostEqual(results[0]['VMAFRC_motion2_score'], 3.895352291666667, places=8)
        self.assertAlmostEqual(results[0]['VMAFRC_adm2_score'], 0.9345877291666667, places=8)
        self.assertAlmostEqual(results[0]['VMAFRC_float_psnr_score'], 30.780577083333331, places=8)
        self.assertAlmostEqual(results[0]['VMAFRC_float_ssim_score'], 0.86322654166666657, places=8)
        self.assertAlmostEqual(results[0]['VMAFRC_float_ms_ssim_score'], 0.9632406874999999, places=8)

        self.assertAlmostEqual(results[1]['VMAFRC_vif_scale0_score'], 1.0, places=8)
        self.assertAlmostEqual(results[1]['VMAFRC_vif_scale1_score'], 0.9999998541666666, places=8)
        self.assertAlmostEqual(results[1]['VMAFRC_vif_scale2_score'], 0.9999996041666667, places=8)
        self.assertAlmostEqual(results[1]['VMAFRC_vif_scale3_score'], 0.9999991458333334, places=8)
        self.assertAlmostEqual(results[1]['VMAFRC_motion2_score'], 3.895352291666667, places=8)
        self.assertAlmostEqual(results[1]['VMAFRC_adm2_score'], 1.0, places=8)
        self.assertAlmostEqual(results[1]['VMAFRC_float_psnr_score'], 72.0, places=8)
        self.assertAlmostEqual(results[1]['VMAFRC_float_ssim_score'], 1.0, places=8)
        self.assertAlmostEqual(results[1]['VMAFRC_float_ms_ssim_score'], 1.0, places=8)

        self.assertAlmostEqual(results[0]['VMAFRC_score'], 76.69926875, places=8)
        self.assertAlmostEqual(results[1]['VMAFRC_score'], 99.94641666666666, places=8)

    def test_run_vmafrc_runner_yuv422p10le_sparks(self):

        ref_path = VmafConfig.test_resource_path("yuv", "sparks_ref_480x270.yuv42010le.yuv")
        dis_path = VmafConfig.test_resource_path("yuv", "sparks_dis_480x270.yuv42010le.yuv")
        asset = Asset(dataset="test", content_id=0, asset_id=0,
                      workdir_root=VmafConfig.workdir_path(),
                      ref_path=ref_path,
                      dis_path=dis_path,
                      asset_dict={'width': 480, 'height': 270,
                                  'yuv_type': 'yuv420p10le'})

        asset_original = Asset(dataset="test", content_id=0, asset_id=1,
                      workdir_root=VmafConfig.workdir_path(),
                      ref_path=ref_path,
                      dis_path=ref_path,
                      asset_dict={'width': 480, 'height': 270,
                                  'yuv_type': 'yuv420p10le'})

        self.runner = VmafrcQualityRunner(
            [asset, asset_original],
            None, fifo_mode=True,
            delete_workdir=True,
            result_store=None,
            optional_dict={
                'psnr': True,
                'ssim': True,
                'ms_ssim': True,
            }
        )
        self.runner.run(parallelize=True)

        results = self.runner.results

        self.assertAlmostEqual(results[0]['VMAFRC_vif_scale0_score'],0.9240746, places=8)
        self.assertAlmostEqual(results[0]['VMAFRC_vif_scale1_score'], 0.9968371999999999, places=8)
        self.assertAlmostEqual(results[0]['VMAFRC_vif_scale2_score'], 0.9987575999999999, places=8)
        self.assertAlmostEqual(results[0]['VMAFRC_vif_scale3_score'], 0.9993221999999999, places=8)
        self.assertAlmostEqual(results[0]['VMAFRC_motion2_score'], 0.7523685999999999, places=8)
        self.assertAlmostEqual(results[0]['VMAFRC_adm2_score'], 0.9981770000000001, places=8)
        self.assertAlmostEqual(results[0]['VMAFRC_float_psnr_score'], 48.81622, places=8)
        self.assertAlmostEqual(results[0]['VMAFRC_float_ssim_score'], 0.99566, places=8)
        self.assertAlmostEqual(results[0]['VMAFRC_float_ms_ssim_score'], 0.9993778000000001, places=8)

        self.assertAlmostEqual(results[1]['VMAFRC_vif_scale0_score'], 1.0, places=8)
        self.assertAlmostEqual(results[1]['VMAFRC_vif_scale1_score'], 0.9999990000000001, places=8)
        self.assertAlmostEqual(results[1]['VMAFRC_vif_scale2_score'], 0.9999990000000001, places=8)
        self.assertAlmostEqual(results[1]['VMAFRC_vif_scale3_score'], 0.9999990000000001, places=8)
        self.assertAlmostEqual(results[1]['VMAFRC_motion2_score'], 0.7523685999999999, places=8)
        self.assertAlmostEqual(results[1]['VMAFRC_adm2_score'], 1.0, places=8)
        self.assertAlmostEqual(results[1]['VMAFRC_float_psnr_score'], 72.0, places=8)
        self.assertAlmostEqual(results[1]['VMAFRC_float_ssim_score'], 1.0, places=8)
        self.assertAlmostEqual(results[1]['VMAFRC_float_ms_ssim_score'], 1.0, places=8)

        self.assertAlmostEqual(results[0]['VMAFRC_score'], 97.90585999999999, places=8)
        self.assertAlmostEqual(results[1]['VMAFRC_score'], 98.47138, places=8)


class VmafrcQualityRunnerSubsamplingTest(unittest.TestCase):

    def tearDown(self):
        if hasattr(self, 'runner0'):
            self.runner0.remove_results()
        if hasattr(self, 'runner'):
            self.runner.remove_results()

    def setUp(self):
        self.result_store = FileSystemResultStore()

    def test_run_vmafrc_runner_with_subsample2(self):

        ref_path, dis_path, asset, asset_original = set_default_576_324_videos_for_testing()

        subsample = 5

        self.runner0 = VmafrcQualityRunner(
            [asset, asset_original],
            None, fifo_mode=True,
            delete_workdir=True,
            result_store=None,
            optional_dict={}
        )
        self.runner0.run()
        results0 = self.runner0.results

        self.runner = VmafrcQualityRunner(
            [asset, asset_original],
            None, fifo_mode=True,
            delete_workdir=True,
            result_store=None,
            optional_dict={'subsample': subsample}
        )
        self.runner.run()
        results = self.runner.results

        for i in range(48):
            if i % subsample == 0:
                self.assertAlmostEqual(results0[0]['VMAFRC_scores'][i], results[0]['VMAFRC_scores'][i // subsample], places=7)
                self.assertAlmostEqual(results0[1]['VMAFRC_scores'][i], results[1]['VMAFRC_scores'][i // subsample], places=7)


class QualityRunnerVersionTest(unittest.TestCase):

    def test_vmafrc_quality_runner_version(self):
        self.assertEqual(VmafrcQualityRunner.VERSION, 'F0.2.4c-0.6.1')
        self.assertEqual(VmafrcQualityRunner.ALGO_VERSION, 2)
