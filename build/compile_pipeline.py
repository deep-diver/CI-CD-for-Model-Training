import os
import logging
import argparse
import create_pipeline

from tfx import v1 as tfx


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--pipeline-name",
        type=str,
    )

    parser.add_argument(
        "--pipeline-root",
        type=str,
    )

    parser.add_argument(
        "--data-root",
        type=str,
    )

    parser.add_argument(
        "--module-root",
        type=str,
    )

    parser.add_argument(
        "--serving-model-dir",
        type=str,
    )
    
    parser.add_argument(
        "--tfx-image-uri",
        type=str,
        required=False,
        default="gcr.io/tfx-oss-public/tfx:0.30.0"
    )

    return parser.parse_args()


def compile_pipeline(args):
    pipeline_definition_file = args.pipeline_name + ".json"

    runner = tfx.orchestration.experimental.KubeflowV2DagRunner(
        config=tfx.orchestration.experimental.KubeflowV2DagRunnerConfig(
                default_image=args.tfx_image_uri
            ),
        output_filename=pipeline_definition_file,
    )

    return runner.run(
        create_pipeline(
            pipeline_name=args.pipeline_name,
            pipeline_root=args.pipeline_root,
            data_root=args.data_root,
            module_file=os.path.join(args.module_root + "penguin_trainer.py"),
            serving_model_dir=args.serving_model_dir,
            project_id=os.getenv("PROJECT"),
            region=os.getenv("REGION"),
            # We will use CPUs only for now.
            use_gpu=False,
        ),
        write_out=True,
    )


def main():
    args = get_args()
    print(f"TFX Version: {tfx.__version__}")
    result = compile_pipeline(args)
    logging.info(result)


if __name__ == "__main__":
    main()
